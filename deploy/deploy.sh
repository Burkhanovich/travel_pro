#!/bin/bash
# =============================================================================
# Travel Pro – Deploy / update script
# Run as the 'travelpro' user (or root with sudo -u travelpro)
# Usage: bash deploy/deploy.sh
# =============================================================================
set -e

APP_DIR="/var/www/travelpro"
VENV="$APP_DIR/.venv"
PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"
MANAGE="$PYTHON $APP_DIR/manage.py"

echo ""
echo "=============================="
echo " Travel Pro – Deploying..."
echo "=============================="

cd $APP_DIR

# --- Pull latest code ---
echo "[1/8] Pulling latest code..."
git pull origin main

# --- Create/update virtual environment ---
echo "[2/8] Updating virtual environment..."
if [ ! -d "$VENV" ]; then
    python3.13 -m venv $VENV
fi
$PIP install --upgrade pip
$PIP install -r requirements/production.txt

# --- Build Tailwind CSS (BEFORE collectstatic, so the fresh CSS is collected) ---
echo "[3/8] Building Tailwind CSS..."
if [ -f "$APP_DIR/package.json" ] && command -v npm >/dev/null 2>&1; then
    cd $APP_DIR
    # The 'travelpro' user's real $HOME (/home/travelpro) isn't writable, so
    # npm ci fails with EACCES trying to create its cache there. Point HOME and
    # the npm cache at the writable app dir. --include=dev ensures the build
    # CLI (@tailwindcss/cli, a devDependency) is installed.
    export HOME="$APP_DIR"
    export npm_config_cache="$APP_DIR/.npm-cache"
    npm ci --include=dev --silent
    npm run css:build
else
    echo "  npm/package.json unavailable — using committed static/css/tailwind.css"
fi

# --- Collect static files ---
echo "[4/8] Collecting static files..."
DJANGO_SETTINGS_MODULE=config.settings.production $MANAGE collectstatic --noinput

# --- Run database migrations ---
echo "[5/8] Running migrations..."
DJANGO_SETTINGS_MODULE=config.settings.production $MANAGE migrate --noinput

# --- Compile translation files ---
echo "[6/8] Compiling translations..."
DJANGO_SETTINGS_MODULE=config.settings.production $MANAGE compilemessages 2>/dev/null || \
    $PYTHON generate_translations.py

# --- Clear cache ---
echo "[7/8] Clearing Redis cache..."
DJANGO_SETTINGS_MODULE=config.settings.production $MANAGE shell -c \
    "from django.core.cache import cache; cache.clear(); print('Cache cleared.')" 2>/dev/null || true

# --- Restart services ---
echo "[8/8] Restarting services..."
sudo systemctl restart travelpro-gunicorn
sudo systemctl restart travelpro-celery
sudo systemctl restart travelpro-celery-beat

echo ""
echo "=============================="
echo " Deploy complete! ✓"
echo "=============================="
echo "Gunicorn : $(sudo systemctl is-active travelpro-gunicorn)"
echo "Celery   : $(sudo systemctl is-active travelpro-celery)"
echo "Beat     : $(sudo systemctl is-active travelpro-celery-beat)"
