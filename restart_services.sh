#!/bin/bash

echo "==============================="
echo "   Restarting Nukestation..."
echo "==============================="

echo ""
echo "→ Reloading Nginx..."
sudo nginx -t
if [ $? -ne 0 ]; then
    echo "❌ ERROR: nginx configuration test failed!"
    exit 1
fi

sudo systemctl reload nginx
echo "✔ Nginx reloaded."

echo ""
echo "→ Restarting Flask Backend (gunicorn)..."
sudo systemctl restart nukestation-backend
sleep 1

sudo systemctl status nukestation-backend --no-pager
echo "✔ Flask backend restarted."

echo ""
echo "==============================="
echo "   All services restarted."
echo "==============================="
