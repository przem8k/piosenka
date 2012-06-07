"""
 Command for database backup
"""

import os, time
from django.core.management.base import BaseCommand

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

        backup_dir = '~/database_backups/piosenka'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        outfile = os.path.join(backup_dir, 'backup_%s.sql' % time.strftime('%y%m%d%S'))

        if self.engine == 'django.db.backends.postgresql_psycopg2':
            print 'Doing Postgresql backup to database %s into %s' % (self.db, outfile)
            self.do_postgresql_backup(outfile)
        else:
            print 'Backup in %s engine not implemented' % self.engine

    def do_postgresql_backup(self, outfile):
        args = []
        if self.user:
            args += ["--username=%s" % self.user]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        if self.db:
            args += [self.db]
        
        if self.host == "sql.adaptivevision.megiteam.pl":
            tool = "/usr/local/pgsql-8.4/bin/pg_dump"
        else:
            tool = "pg_dump"
                
        command = '%s %s > %s' % (tool, ' '.join(args), outfile)
        print command
        os.system(command)
