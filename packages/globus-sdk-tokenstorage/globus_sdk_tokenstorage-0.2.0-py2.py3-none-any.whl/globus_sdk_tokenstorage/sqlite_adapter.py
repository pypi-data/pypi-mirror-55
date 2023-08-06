import json
import os
import sqlite3

from .abstract_base import AbstractStorageAdapter
from .version import __version__


class SQLiteAdapter(AbstractStorageAdapter):
    """
    :param dbname: the name of the DB file to write to and read from
    :param namespace: A "namespace" to use within the database. All operations will
                      be performed indexed under this string, so that multiple distinct
                      sets of tokens may be stored in the database. You might use
                      usernames as the namespace to implement a multi-user system, or
                      profile names to allow multiple Globus accounts to be used by a
                      single user.

    A storage adapter for storing tokens in sqlite databases.

    SQLite adapters are for more complex cases, where there may be multiple users or
    "profiles" in play, and additionally a dynamic set of resource servers which need to
    be stored in an extensible way.

    The ``namespace`` is a user-supplied way of partitioning data, and any token
    responses passed to the storage adapter are broken apart and stored indexed by
    *resource_server*. If you have a more complex use-case in which this scheme will be
    insufficient, you should encode that in your choice of ``namespace`` values.
    """

    def __init__(self, dbname, namespace="DEFAULT"):
        self.dbname = dbname
        self.namespace = namespace
        self._connection = self._init_and_connect()

    def _init_and_connect(self):
        init_tables = self.dbname == ":memory:" or not os.path.exists(self.dbname)
        conn = sqlite3.connect(self.dbname)
        if init_tables:
            conn.executescript(
                """
CREATE TABLE config_storage (
    namespace VARCHAR NOT NULL,
    config_name VARCHAR NOT NULL,
    config_data_json VARCHAR NOT NULL,
    PRIMARY KEY (namespace, config_name)
);
CREATE TABLE token_storage (
    namespace VARCHAR NOT NULL,
    resource_server VARCHAR NOT NULL,
    token_data_json VARCHAR NOT NULL,
    PRIMARY KEY (namespace, resource_server)
);
CREATE TABLE sdk_storage_adapter_internal (
    attribute VARCHAR NOT NULL,
    value VARCHAR NOT NULL,
    PRIMARY KEY (attribute)
);
            """
            )
            # mark the version which was used to create the DB
            # also mark the "database schema version", useful for upgrades
            conn.executemany(
                """
INSERT INTO sdk_storage_adapter_internal(attribute, value) VALUES (?, ?);
            """,
                [
                    ("globus-sdk-tokenstorage.version", __version__),
                    ("globus-sdk-tokenstorage.database_schema_version", "1"),
                ],
            )
            conn.commit()
        return conn

    def store_config(self, config_name, config_dict):
        """
        :param config_name: A string name for the configuration value
        :param config_dict: A dict of config which will be stored serialized as JSON

        Store a config dict under the current namespace in the config table.
        Allows arbitrary configuration data to be namespaced under the namespace, so
        that application config may be associated with the stored tokens.

        Uses sqlite "REPLACE" to perform the operation.
        """
        self._connection.execute(
            """
REPLACE INTO config_storage(namespace, config_name, config_data_json)
VALUES (?, ?, ?)
            """,
            (self.namespace, config_name, json.dumps(config_dict)),
        )
        self._connection.commit()

    def read_config(self, config_name):
        """
        :param config_name: A string name for the configuration value

        Load a config dict under the current namespace in the config table.
        If no value is found, returns None
        """
        row = self._connection.execute(
            """
SELECT config_data_json FROM config_storage WHERE namespace=? AND config_name=?
        """,
            (self.namespace, config_name),
        ).fetchone()

        if row is None:
            return None
        config_data_json = row[0]
        return json.loads(config_data_json)

    def store(self, token_response):
        """
        By default, ``self.on_refresh`` is just an alias for this function.

        Given a token response, extract the token data for the resource servers and
        write it to ``self.dbname``, stored under the adapter's namespace
        """
        pairs = []
        for rs_name, token_data in token_response.by_resource_server.items():
            pairs.append((rs_name, token_data))

        self._connection.executemany(
            """
REPLACE INTO token_storage(namespace, resource_server, token_data_json)
VALUES(?, ?, ?);
            """,
            [
                (self.namespace, rs_name, json.dumps(token_data))
                for (rs_name, token_data) in pairs
            ],
        )
        self._connection.commit()

    def read_as_dict(self):
        """
        Load the token data JSON and return the resulting dict objects, indexed by
        resource server.
        This should look identical to an OAuthTokenResponse.by_resource_server in format
        and content. (But it is not attached to a token response object.)
        """
        data = {}
        for row in self._connection.execute(
            """
SELECT resource_server, token_data_json FROM token_storage WHERE namespace=?
        """,
            (self.namespace,),
        ):
            resource_server, token_data_json = row
            data[resource_server] = json.loads(token_data_json)
        return data
