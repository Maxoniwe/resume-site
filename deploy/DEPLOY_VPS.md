# Deploy to VPS

## 1. Install system packages on the server

```bash
sudo apt update
sudo apt install -y python3 python3-venv nginx certbot python3-certbot-nginx
```

## 2. Create directories on the server

```bash
sudo mkdir -p /srv/resume_site/app
sudo chown -R $USER:$USER /srv/resume_site
```

## 3. Upload the project from Windows PowerShell

Replace placeholders with your own values:
- `<server_user>`: your SSH login
- `<server_ip>`: your server IP
- `<project_domain>`: your domain

```powershell
scp -r D:\Dev\config D:\Dev\resume D:\Dev\scripts D:\Dev\deploy D:\Dev\manage.py D:\Dev\requirements.txt D:\Dev\requirements-prod.txt D:\Dev\gunicorn.conf.py D:\Dev\.env.example <server_user>@<server_ip>:/srv/resume_site/app/
scp D:\Dev\db.sqlite3 <server_user>@<server_ip>:/srv/resume_site/app/
scp -r D:\Dev\media <server_user>@<server_ip>:/srv/resume_site/app/
```

## 4. Create a virtual environment on the server

```bash
cd /srv/resume_site/app
python3 -m venv /srv/resume_site/.venv
source /srv/resume_site/.venv/bin/activate
pip install --upgrade pip
pip install -r requirements-prod.txt
```

## 5. Create the production env file

```bash
sudo cp /srv/resume_site/app/.env.example /etc/resume_site.env
sudo nano /etc/resume_site.env
```

Recommended values:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=put-a-long-random-secret-here
DJANGO_ALLOWED_HOSTS=<project_domain>,<server_ip>
DJANGO_CSRF_TRUSTED_ORIGINS=https://<project_domain>,http://<project_domain>
DJANGO_SQLITE_PATH=/srv/resume_site/app/db.sqlite3
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
```

## 6. Run migrations and collect static files

```bash
cd /srv/resume_site/app
source /srv/resume_site/.venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

## 7. Install systemd service

```bash
sudo cp deploy/systemd/resume-site.service /etc/systemd/system/resume-site.service
sudo systemctl daemon-reload
sudo systemctl enable resume-site
sudo systemctl start resume-site
sudo systemctl status resume-site
```

## 8. Install Nginx config

```bash
sudo cp deploy/nginx/resume.serveblog.net.conf /etc/nginx/sites-available/<project_domain>.conf
sudo ln -s /etc/nginx/sites-available/<project_domain>.conf /etc/nginx/sites-enabled/<project_domain>.conf
sudo nginx -t
sudo systemctl reload nginx
```

## 9. Issue SSL certificate

```bash
sudo certbot --nginx -d <project_domain>
```

After the certificate is active, update `/etc/resume_site.env`:

```env
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=31536000
```

Then restart the app:

```bash
sudo systemctl restart resume-site
```

## 10. Useful commands

```bash
sudo systemctl restart resume-site
sudo systemctl status resume-site
sudo journalctl -u resume-site -n 100 --no-pager
sudo nginx -t
```
