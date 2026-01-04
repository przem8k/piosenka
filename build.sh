set -e
rm -rf out
mkdir out
python manage.py compress --force
python manage.py collectstatic --noinput
RELEASE=1 python manage.py gen