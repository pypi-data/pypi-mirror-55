# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import contextlib
import logging
import sqlite3
import threading
import uuid
from time import time

from p2p0mq.constants import TRACE, SYNC_DB_INTERVAL
from p2p0mq.peer import Peer


logger = logging.getLogger('p2p0mq.app')

SQLITE_PEERS_TABLE = 'p2p0mq_peers'
SQLITE_META_TABLE = 'p2p0mq_meta'


class PeerStore(object):
    """
    Given an sqlite database, read it from time to time
    and merge the settings found there with the ones found
    in memory.
    """
    def __init__(self, db_file_path=None, app_uuid=None, *args, **kwargs):
        """ Constructor. """
        super(PeerStore, self).__init__(*args, **kwargs)
        self.db_file_path = db_file_path
        self.peers = {}
        self.peers_lock = threading.Lock()

        self.next_peer_db_sync_time = time() - SYNC_DB_INTERVAL

        # Metadata.
        self._uuid = None
        if app_uuid is not None:
            assert len(app_uuid) > 4
            self.uuid = app_uuid
        self.db_created = None

        logger.debug("Using database %s", self.db_file_path)

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if isinstance(value, str):
            self._uuid = value.encode()
        elif isinstance(value, bytes):
            self._uuid = value
        elif isinstance(value, int):
            self._uuid = ('%r' % value).encode()
        else:
            raise ValueError("uuid needs to be a string")
        if len(self._uuid) < 4:
            raise ValueError("uuid needs to be at least 4 characters long")

    def add_peer(self, peer):
        """ Adds a peer from code (database does not call this method). """
        with self.peers_lock:
            self.peers[peer.uuid] = peer

    def take_peer(self, peer):
        """ Removes a peer (database does not call this method). """
        with self.peers_lock:
            return self.peers.pop(
                peer.uuid if isinstance(peer, Peer) else peer)

    @property
    def peers_in_initial_state(self):
        with self.peers_lock:
            return [peer for peer in self.peers.values()
                    if peer.state_initial]

    @property
    def peers_connected(self):
        with self.peers_lock:
            return [peer for peer in self.peers.values()
                    if peer.state_connected]

    @property
    def peers_routed(self):
        with self.peers_lock:
            return [peer for peer in self.peers.values()
                    if peer.state_routed]

    @property
    def peers_unreachable(self):
        with self.peers_lock:
            return [peer for peer in self.peers.values()
                    if peer.state_unreachable]

    def start_db(self):
        """ Called when an app is doen with this instance. """
        self.read_metadata()
        assert self.uuid is not None
        self.sync_database(force=True)

    def terminate_db(self):
        """
        Called when an app is done with this instance.

        This method should be written defensively, as the environment
        might not be fully set (an exception in create() does not prevent
        this method from being executed).
        """
        pass

    def table_exists(self, c, name):
        """ Tells if our table exists in the database. """
        c.execute(
            "SELECT name FROM sqlite_master "
            "    WHERE type='table' "
            "    AND name=?;",
            (name, ))
        result = c.fetchone()
        if result is None:
            return False
        return len(result) > 0

    def create_peers_table(self, c):
        """ Creates the table into the database. """
        c.execute(
            "CREATE TABLE %s ("
            "    peer_id INTEGER PRIMARY KEY,"
            "    uuid TEXT,"
            "    host TEXT,"
            "    port INTEGER"
            ")" % SQLITE_PEERS_TABLE)

    def create_meta_table(self, c):
        """ Creates the table into the database. """
        c.execute(
            "CREATE TABLE %s ("
            "    id INTEGER PRIMARY KEY,"
            "    key TEXT UNIQUE,"
            "    value TEXT,"
            "    description TEXT"
            ")" % SQLITE_META_TABLE)
        self.uuid = uuid.uuid4().hex if self.uuid is None else self.uuid
        self.db_created = time()
        c.executemany(
            "INSERT INTO %s(key,value,description) "
            "    VALUES(?, ?, ?);" % SQLITE_META_TABLE,
            (
                ('uuid', self.uuid,
                 'the unique identification of this instance'),
                ('db_created', self.db_created,
                 'the time when the metadata was inserted'),
            ))

    def read_metadata(self):
        logger.log(TRACE, "Reading database %s metadata", self.db_file_path)
        with contextlib.closing(
                sqlite3.connect(
                    self.db_file_path,
                    uri=self.db_file_path.startswith("file:"))) as conn:
            try:
                c = conn.cursor()
                if not self.table_exists(c, SQLITE_META_TABLE):
                    self.create_meta_table(c)
                    conn.commit()
                    return

                c.execute(
                    "SELECT id, key, value FROM %s;" % SQLITE_META_TABLE)
                for row in c.fetchall():
                    setattr(self, row[1], row[2])
            except conn.Error:
                conn.rollback()

    def sync_database(self, force=False):
        """ Synchronizes the content of the memory with the database. """
        if (self.next_peer_db_sync_time > time()) and not force:
            return None

        logger.log(TRACE, "Synchronizing the list of peers with the "
                          "content of the database")
        with contextlib.closing(
                sqlite3.connect(
                    self.db_file_path,
                    uri=self.db_file_path.startswith("file:"))) as conn:

            c = conn.cursor()
            if not self.table_exists(c, SQLITE_PEERS_TABLE):
                self.create_peers_table(c)
                return None

            # Collect peers that are in database but not in memory.
            database_peers = {}
            new_peers = {}
            c.execute(
                "SELECT peer_id, uuid, host, port FROM %s;" %
                SQLITE_PEERS_TABLE)

            with self.peers_lock:
                for row in c.fetchall():
                    peer = Peer(
                        uuid=row[1], db_id=row[0],
                        host=row[2], port=row[3])
                    if peer.uuid in self.peers:
                        database_peers[peer.uuid] = peer
                    else:
                        new_peers[peer.uuid] = peer

                # Save peers that are only present in the memory.
                saved_peer_count = 0
                for peer in self.peers.values():
                    if peer.uuid not in database_peers:
                        assert peer.db_id is None
                        c.execute(
                            "INSERT INTO %s(uuid,host,port) "
                            "    VALUES(?, ?, ?);" % SQLITE_PEERS_TABLE,
                            (peer.uuid, peer.host, peer.port)
                        )
                        peer.db_id = c.lastrowid
                        saved_peer_count = saved_peer_count + 1

                # Integrate new peers.
                self.peers.update(new_peers)

            conn.commit()

        logger.log(TRACE, "Database has been synchronized. "
                          "%d loaded peers, %d saved peers, "
                          "%d total peers",
                   len(new_peers), saved_peer_count, len(self.peers)
                   )
        self.next_peer_db_sync_time = time() + SYNC_DB_INTERVAL
        return new_peers

