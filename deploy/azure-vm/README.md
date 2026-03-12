# Azure VM deployment

These files assume an Ubuntu-based Azure VM that serves:

- Django with Gunicorn on `127.0.0.1:8000`
- React/Vite static build from `frontend/dist`
- Nginx as the public web server and reverse proxy

## Suggested layout

```text
/var/www/milkman/
  backend/
  frontend/
```

## 1. Install system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx postgresql postgresql-contrib nodejs npm
```

## 2. Configure app environment

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Update `backend/.env` with your real domain, IP, secret key, and database credentials.

## 3. Build and prepare the app

```bash
bash deploy/azure-vm/scripts/deploy_backend.sh
bash deploy/azure-vm/scripts/build_frontend.sh
```

## 4. Install systemd service

```bash
sudo cp deploy/azure-vm/systemd/milkman-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable milkman-backend
sudo systemctl restart milkman-backend
sudo systemctl status milkman-backend
```

If your VM user is not `www-data`, update `User`, `Group`, `WorkingDirectory`, `EnvironmentFile`, and `ExecStart` in the service file before copying it.

## 5. Install Nginx site

```bash
sudo cp deploy/azure-vm/nginx/milkman.conf /etc/nginx/sites-available/milkman
sudo ln -sf /etc/nginx/sites-available/milkman /etc/nginx/sites-enabled/milkman
sudo nginx -t
sudo systemctl restart nginx
```

Update `server_name` and the `/var/www/milkman/...` paths in the Nginx config if your VM uses a different domain or folder.

## 6. Azure networking

- Open inbound TCP ports `80` and `443` in the Azure VM network security group.
- If you keep PostgreSQL on the same VM, leave port `5432` closed publicly.
- Point your domain DNS `A` record to the VM public IP.

## 7. HTTPS

After HTTP works, install TLS with Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Then set these in `backend/.env` and restart Gunicorn:

```bash
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SECURE_HSTS_PRELOAD=True
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```
