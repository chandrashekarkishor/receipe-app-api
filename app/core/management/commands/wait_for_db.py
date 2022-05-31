"""
Django command to wait for db to connect and available before connection to db.
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for db
    """

    def handle(self, *args, **options):
        """
        Entrypoint for command
        :param args:
        :param options:
        :return:
        """
        self.stdout.write("Waiting for database")
        db_up = False
        while not db_up:
            try:
                self.check(
                    databases=['default'])
                # check is internal method of Base command
                # to check availability of dB
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting for 1 sec")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database Available"))
