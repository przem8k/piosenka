"""
 Command for backing up the db and site media.
"""

from io import StringIO
import os
import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Back up the site in the cloud.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            help='Print commands instead of executing them.',
        )

    def handle(self, *args, **options):
        # Workaround running from cron encoding problems. Is it still needed?
        # sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
        self.dry_run = options['dry_run']
        backup_name = time.strftime('%y%m%d-%H%M%S')
        backup_root = os.path.join(os.environ['HOME'], 'backup')
        directory = os.path.join(backup_root, backup_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # SQL.
        sql_file_name = 'postgres_' + backup_name + '.tar'
        sql_file_path = os.path.join(settings.TMP_DIR, sql_file_name)
        self.dump_sql(sql_file_path)

        sql_remote_path = 'db/' + sql_file_name
        self.upload_object(sql_file_path, sql_remote_path)

        # Media.
        media_remote_path = 'media'
        self.upload_directory(settings.MEDIA_ROOT, media_remote_path)

    def dump_sql(self, out_file_path):
        engine = settings.DATABASES['default']['ENGINE']
        db = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']

        command = ['pg_dump']
        command += ['--username=%s' % user]
        command += ['--host=%s' % host]
        command += ['--port=%s' % port]
        command += ['--format=t']  # Use tarball backup format.
        command += ['--clean']  # When restoring, start with cleaning the database.
        command += ['--file=' +  out_file_path]
        command += [db]
        if self.dry_run:
            print(command)
            return
        subprocess.run(command, check=True)

    def upload_object(self, local_path, remote_path):
        destination = 'gs://%s/%s' % (settings.GCP_STORAGE_BUCKET, remote_path)
        command = [settings.GSUTIL_PATH, 'cp', local_path, destination]
        if self.dry_run:
            print(command)
            return
        subprocess.run(command, check=True)

    def upload_directory(self, local_path, remote_path):
        destination = 'gs://%s/%s' % (settings.GCP_STORAGE_BUCKET, remote_path)
        command = [settings.GSUTIL_PATH, 'rsync', '-r', local_path, destination]
        if self.dry_run:
            print(command)
            return
        subprocess.run(command, check=True)
