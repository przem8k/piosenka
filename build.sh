set -e

# TEMP (squash before merge): build stamp shown in the footer so we can
# see which build is live and whether a device's service worker is stale.
export BUILD_ID="${BUILD_ID:-$(git rev-parse --short HEAD 2>/dev/null || echo dev)-$(date -u +%H%M%S)}"

rm -rf out
mkdir out
python manage.py compress --force
python manage.py collectstatic --noinput
RELEASE=1 python manage.py gen
npm run --silent build:sw
