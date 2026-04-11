# Django Resume Site

A clean Django starter for a personal resume or portfolio website.

The homepage content is editable through the Django admin panel, so this repository works well as a base project that you can clone and customize with your own profile, experience, projects, and contact details.

## Features

- Editable homepage content through Django admin
- Skills, experience, projects, achievements, and social links
- Optional profile photo and downloadable resume file
- PDF resume export endpoint
- Static file support for local use and deployment
- Starter deployment files for Vercel and VPS environments

## Tech Stack

- Python
- Django 4.2
- Pillow
- WhiteNoise
- Gunicorn

## Quick Start

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Apply migrations:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Load starter content:

```powershell
.\.venv\Scripts\python.exe manage.py loaddata resume/fixtures/vercel_content.json
```

Create an admin user:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Run the dev server:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## What You Can Customize

- Intro section
- About block
- Skills
- Experience timeline
- Project cards
- Achievements
- Contact details
- Social links
- Profile image
- Resume PDF / CV file

Most content can be updated directly from the admin panel after setup.

## Important Before Publishing

Replace the demo content with your own data before making the site public:

- name and job title
- email and phone
- social links
- project descriptions
- profile photo
- resume file

If you store personal files locally, keep them out of git unless you explicitly want them in the repository.

## Deployment

### Vercel

The repository includes `vercel.json` and `api/index.py` for Vercel deployment.

### VPS

Starter deployment files for Gunicorn, systemd, and Nginx are included in:

- `deploy/DEPLOY_VPS.md`
- `deploy/systemd/resume-site.service`
- `deploy/nginx/resume.serveblog.net.conf`

## Useful Commands

Run checks:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

Run tests:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

## Notes

- The fixture file provides generic starter content so the site is not empty after setup.
- Media files should be added by each project owner separately.
- This repository is intended to be used as a customizable base, not as a personal data dump.
