from pathlib import Path
import os
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.core.management import call_command
from django.conf import settings


django.setup()

from resume.models import ResumeProfile
from resume.pdf_export import build_resume_pdf
from resume.views import get_resume_context


FIXTURE_PATH = BASE_DIR / 'resume' / 'fixtures' / 'vercel_content.json'


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def seed_content_if_needed():
    if not env_bool('DJANGO_LOAD_VERCEL_FIXTURE', True):
        print('Skipping fixture load because DJANGO_LOAD_VERCEL_FIXTURE is disabled.')
        return

    if not FIXTURE_PATH.exists():
        print(f'Skipping fixture load because {FIXTURE_PATH} does not exist.')
        return

    if ResumeProfile.objects.exists():
        print('Skipping fixture load because resume content already exists.')
        return

    print(f'Loading fixture: {FIXTURE_PATH}')
    call_command('loaddata', str(FIXTURE_PATH))


def main():
    print('Running Django migrations for Vercel build...')
    call_command('migrate', interactive=False, verbosity=1)
    seed_content_if_needed()
    print('Collecting static files...')
    call_command('collectstatic', interactive=False, verbosity=1)
    print('Generating prebuilt PDF for Vercel runtime...')
    context = get_resume_context()
    pdf_bytes = build_resume_pdf(
        profile=context['profile'],
        skills=context['skills'],
        experiences=context['experiences'],
        projects=context['projects'],
        achievements=context['achievements'],
        social_links=context['social_links'],
    )
    output_path = settings.STATIC_ROOT / 'generated' / 'resume.pdf'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    print(f'Prebuilt PDF saved to: {output_path}')
    print('Vercel build preparation finished.')


if __name__ == '__main__':
    main()
