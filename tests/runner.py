"""Module for running django project tests."""
from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """Creator of database.

    Args:
        self: db connection stuff
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS databank;')


class PostgresSchemaRunner(DiscoverRunner):
    """Postgres db schema creator and runner.

    Args:
        DiscoverRunner (_type_): django inheritance for runner creation
    """

    def setup_databases(
        self, **kwargs: Any,
    ) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """Runner of database setup.

        Args:
            kwargs: basic kwargs for db setup

        Returns:
            list[tuple[BaseDatabaseWrapper, str, bool]]: list of db wrappers
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
