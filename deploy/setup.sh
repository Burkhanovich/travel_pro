#!/bin/bash
# =============================================================================
# Travel Pro – First-time server setup script
# Run as root on a fresh Ubuntu 22.04 / 24.04 server
# Usage: sudo bash setup.sh
# =============================================================================
set -e

APP_USER="travelpro"
APP_DIR="/var/www/travelpro"
LOG_DIR="/var/log/travelpro"
RUN_DIR="/run/travelpro"
PYTHON_VERSION="3.13"

echo "=============================="
echo " Travel Pro Server Setup"
echo "=============================="

# --- System packages ---
apt-get update
apt-get install -y \
    python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python3-pip \
    postgresql postgresql-contrib \
    redis-server \
    nginx \
    certbot python3-certbot-nginx \
    git curl build-essential libpq-dev \
    supervisor

# --- Create app user ---
if ! id "$APP_USER" &>/dev/null; then
    useradd --system --shell /bin/bash --home $APP_DIR --create-home $APP_USER
    echo "User '$APP_USER' created."
fi

# --- Directories ---
mkdir -p $LOG_DIR $RUN_DIR
chown $APP_USER:$APP_USER $LOG_DIR $RUN_DIR
chmod 750 $LOG_DIR

# --- Log rotation ---
cat > /etc/logrotate.d/travelpro << 'EOF'
/var/log/travelpro/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 travelpro travelpro
    sharedscripts
    postrotate
        systemctl reload travelpro-gunicorn 2>/dev/null || true
    endscript
}
EOF

# --- PostgreSQL: create DB + user ---
echo "Creating PostgreSQL database..."
sudo -u postgres psql << 'PSQL'
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'travelpro') THEN
        CREATE USER travelpro WITH PASSWORD 'CHANGE_THIS_PASSWORD';
    END IF;
END$$;
CREATE DATABASE travelpro_db OWNER travelpro;
GRANT ALL PRIVILEGES ON DATABASE travelpro_db TO travelpro;
PSQL
echo "Database created. Set password in .env"

# --- Redis: bind to localhost only ---
sed -i 's/^bind .*/bind 127.0.0.1 ::1/' /etc/redis/redis.conf
systemctl restart redis-server
systemctl enable redis-server

# --- systemd tmpfiles for /run/travelpro ---
cat > /etc/tmpfiles.d/travelpro.conf << EOF
d /run/travelpro 0755 $APP_USER $APP_USER -
EOF
systemd-tmpfiles --create /etc/tmpfiles.d/travelpro.conf

# --- Copy systemd service files ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp $SCRIPT_DIR/gunicorn.service    /etc/systemd/system/travelpro-gunicorn.service
cp $SCRIPT_DIR/celery.service      /etc/systemd/system/travelpro-celery.service
cp $SCRIPT_DIR/celery-beat.service /etc/systemd/system/travelpro-celery-beat.service
systemctl daemon-reload

echo ""
echo "=============================="
echo " Setup complete!"
echo "=============================="
echo "Next steps:"
echo "  1. Clone your repo to $APP_DIR"
echo "  2. Copy .env.production to $APP_DIR/.env and fill in values"
echo "  3. Run: sudo -u $APP_USER bash $APP_DIR/deploy/deploy.sh"
echo "  4. Configure nginx: cp deploy/nginx.conf /etc/nginx/sites-available/travelpro"
echo "  5. Update domain in nginx.conf, then: certbot --nginx -d yourdomain.com"
echo "  6. Enable services:"
echo "     systemctl enable --now travelpro-gunicorn"
echo "     systemctl enable --now travelpro-celery"
echo "     systemctl enable --now travelpro-celery-beat"
