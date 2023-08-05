"""
    Copyright 2019 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import logging
from typing import Dict, List, Optional

import asyncpg

from inmanta import data
from inmanta.server import SLICE_DATABASE
from inmanta.server import config as opt
from inmanta.server import protocol
from inmanta.types import ArgumentTypes

LOGGER = logging.getLogger(__name__)


class DatabaseService(protocol.ServerSlice):
    """Slice to initialize the database"""

    def __init__(self) -> None:
        super(DatabaseService, self).__init__(SLICE_DATABASE)
        self._pool: Optional[asyncpg.pool.Pool] = None

    async def start(self) -> None:
        await super().start()
        await self.connect_database()

    async def stop(self) -> None:
        await self.disconnect_database()
        self._pool = None
        await super().stop()

    def get_dependencies(self) -> List[str]:
        return []

    async def connect_database(self) -> None:
        """ Connect to the database
        """
        database_host = opt.db_host.get()
        database_port = opt.db_port.get()

        database_username = opt.db_username.get()
        database_password = opt.db_password.get()
        connection_pool_min_size = opt.db_connection_pool_min_size.get()
        connection_pool_max_size = opt.db_connection_pool_max_size.get()
        connection_timeout = opt.db_connection_timeout.get()
        self._pool = await data.connect(
            database_host,
            database_port,
            opt.db_name.get(),
            database_username,
            database_password,
            connection_pool_min_size=connection_pool_min_size,
            connection_pool_max_size=connection_pool_max_size,
            connection_timeout=connection_timeout,
        )
        LOGGER.info("Connected to PostgreSQL database %s on %s:%d", opt.db_name.get(), database_host, database_port)

    async def disconnect_database(self) -> None:
        """ Disconnect the database
        """
        await data.disconnect()

    async def get_status(self) -> Dict[str, ArgumentTypes]:
        """ Get the status of the database connection
        """
        status = {"connected": self._pool is not None, "database": opt.db_name.get(), "host": opt.db_host.get()}

        if self._pool is not None:
            status["max_pool"] = self._pool._maxsize
            status["open_connections"] = (
                len([x for x in self._pool._holders if x._con is not None and not x._con.is_closed()]),
            )

        return status
