set -e
rm -rf static
python manage.py compress --force
python manage.py gen
python manage.py collectstatic --noinput
rm -rf out
RELEASE=1 python manage.py gen