"""
 Command for site backup in the cloud.
"""

from io import StringIO
import os
import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Backup the site in the cloud."

    def handle(self, *args, **options):
        # Workaround running from cron encoding problems.
        sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

        self.engine = settings.DATABASES['default']['ENGINE']
        self.db = settings.DATABASES['default']['NAME']
        self.user = settings.DATABASES['default']['USER']
        self.passwd = settings.DATABASES['default']['PASSWORD']
        self.host = settings.DATABASES['default']['HOST']
        self.port = settings.DATABASES['default']['PORT']
        assert self.engine == 'django.db.backends.postgresql_psycopg2'

        backup_name = time.strftime('%y%m%d-%H%M%S')
        backup_root = os.path.join(os.environ['HOME'], 'backup')
        directory = os.path.join(backup_root, backup_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

#SQL
        sql_file_path = os.path.join(directory,
                                     'postgres_' + backup_name + ".tar")
        print('Doing Postgresql backup to database %s into %s' %
              (self.db, sql_file_path))
        self.dump_sql(sql_file_path)

        # App fixtures
        apps = settings.INSTALLED_APPS
        for app in [elem.split('.')[-1] for elem in apps]:
            json_file_path = os.path.join(
                directory, 'fixture_' + app + '_' + backup_name + ".json")
            self.dump_app_fixture(app, json_file_path)

# Total fixture
        json_file_path = os.path.join(directory,
                                      'fixture_' + backup_name + ".json")
        self.dump_total_fixture(json_file_path)

        push_command = "aws s3 cp %s %sdb/%s/ --recursive" % (
            directory, settings.S3BUCKET, backup_name)
        os.system(push_command)
        print(push_command)

        # Upload sync
        upload_root = settings.MEDIA_ROOT
        upload_command = "aws s3 sync %s %supload/" % (upload_root,
                                                       settings.S3BUCKET,)

        os.system(upload_command)
        print(upload_command)

    def dump_sql(self, out_file_path):
        assert self.user
        assert self.db

        args = []
        args += ["--username=%s" % self.user]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        args += ["--format=t"]  # Use tarball backup format.
        args += ["--clean"]  # When restoring, start with cleaning the database.
        args += [self.db]
        command = 'pg_dump %s > %s' % (' '.join(args), out_file_path)
        print(command)
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
