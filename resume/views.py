from urllib.parse import quote
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.text import slugify

from .models import Achievement, Experience, Project, ResumeProfile, Skill, SocialLink
from .pdf_export import build_resume_pdf


def get_resume_context():
    profile = ResumeProfile.objects.first() or ResumeProfile()
    return {
        'profile': profile,
        'skills': Skill.objects.all(),
        'experiences': Experience.objects.all(),
        'projects': Project.objects.all(),
        'achievements': Achievement.objects.all(),
        'social_links': SocialLink.objects.all(),
    }


def home(request):
    context = get_resume_context()
    return render(request, 'resume/home.html', context)


def download_resume_pdf(request):
    context = get_resume_context()
    profile = context['profile']

    prebuilt_pdf = Path(settings.STATIC_ROOT) / 'generated' / 'resume.pdf'
    if getattr(settings, 'ON_VERCEL', False) and prebuilt_pdf.exists():
        pdf_bytes = prebuilt_pdf.read_bytes()
    else:
        pdf_bytes = build_resume_pdf(
            profile=profile,
            skills=context['skills'],
            experiences=context['experiences'],
            projects=context['projects'],
            achievements=context['achievements'],
            social_links=context['social_links'],
        )

    ascii_root = slugify(profile.full_name) or 'resume'
    unicode_root = slugify(profile.full_name, allow_unicode=True) or ascii_root
    ascii_filename = f'{ascii_root}-resume.pdf'
    download_filename = f'{unicode_root}-resume.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="{ascii_filename}"; '
        f"filename*=UTF-8''{quote(download_filename)}"
    )
    return response
