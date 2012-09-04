"""
 Command for database backup
"""

import os
import time
from StringIO import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Backup database. Only Postgresql engine is implemented"

    def handle(self, *args, **options):
        from django.db import connection
        from django.conf import settings

        self.engine = settings.DATABASES['default']['ENGINE']
        self.db = settings.DATABASES['default']['NAME']
        self.user = settings.DATABASES['default']['USER']
        self.passwd = settings.DATABASES['default']['PASSWORD']
        self.host = settings.DATABASES['default']['HOST']
        self.port = settings.DATABASES['default']['PORT']

        backup_name = time.strftime('%y%m%d-%H%M%S')

        backup_root = os.path.join(os.environ['HOME'], 'backup/piosenka')
        directory = os.path.join(backup_root, backup_name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        #SQL
        sql_file_path = os.path.join(directory, 'postgres_' + backup_name + ".sql")

        if self.engine == 'django.db.backends.postgresql_psycopg2':
            print 'Doing Postgresql backup to database %s into %s' % (self.db, sql_file_path)
            self.dump_sql(sql_file_path)
        else:
            print 'Backup in %s engine not implemented' % self.engine

        # App fixtures
        apps = settings.INSTALLED_APPS
        for app in [elem.split('.')[-1] for elem in apps]:
            json_file_path = os.path.join(directory, 'fixture_' + app + '_' + backup_name + ".json")
            self.dump_app_fixture(app, json_file_path)

        # Total fixture
        json_file_path = os.path.join(directory, 'fixture_' + backup_name + ".json")
        self.dump_total_fixture(json_file_path)

        push_command = "s3cmd sync %s %sdb/" % (directory, settings.S3BUCKET)
        os.system(push_command)
        print push_command

        # Upload sync
        upload_root = settings.MEDIA_ROOT
        upload_command = "s3cmd sync %s %s" % (upload_root, settings.S3BUCKET, )

        os.system(upload_command)
        print upload_command


    def dump_sql(self, out_file_path):
        args = []
        if self.user:
            args += ["--username=%s" % self.user]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        if self.db:
            args += [self.db]

        if self.host == "sql.dxhp.megiteam.pl":
            tool = "/usr/local/pgsql-8.4/bin/pg_dump"
        else:
            tool = "pg_dump"

        command = '%s %s > %s' % (tool, ' '.join(args), out_file_path)
        print command
        os.system(command)

    def dump_app_fixture(self, app, out_file_path):
        json_dump = StringIO()
        call_command("dumpdata", app, stdout=json_dump)
        json_dump.seek(0)

        outfile = open(out_file_path, "w")
        outfile.write(json_dump.read())
        outfile.close()

    def dump_total_fixture(self, out_file_path):
        json_dump = StringIO()
        call_command("dumpdata", stdout=json_dump)
        json_dump.seek(0)

        outfile = open(out_file_path, "w")
        outfile.write(json_dump.read())
        outfile.close()
