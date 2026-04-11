from django.test import TestCase
from django.urls import reverse

from .models import Achievement, Experience, Project, ResumeProfile, Skill, SocialLink


class ResumePdfDownloadTests(TestCase):
    def setUp(self):
        ResumeProfile.objects.all().delete()
        Skill.objects.all().delete()
        Experience.objects.all().delete()
        Achievement.objects.all().delete()
        Project.objects.all().delete()
        SocialLink.objects.all().delete()

        ResumeProfile.objects.create(
            full_name='Maxim Roslyakov',
            job_title='Python Backend Developer',
            resume_title='Backend Python Resume',
            hero_summary='I build Django services, APIs and production-ready integrations.',
            about_title='About me',
            about_text='Focused on backend development, testing and reliable deployments.',
            skills_title='Skills',
            experience_title='Experience',
            achievements_title='Achievements',
            projects_title='Projects',
            contact_title='Contacts',
            contact_note='Reach out for backend roles and freelance projects.',
            email='maxim@example.com',
            phone='+79990000000',
            location='Moscow, Russia',
            download_button_text='Download resume',
        )
        Skill.objects.create(
            title='Django',
            description='Build REST APIs and admin-driven products.',
            icon_label='DJ',
            sort_order=1,
        )
        Experience.objects.create(
            role='Backend Developer',
            company='Acme',
            period='2024 - Present',
            location='Remote',
            summary='Developed backend services and integrations.',
            highlights='Built REST APIs\nCovered business logic with tests',
            sort_order=1,
        )
        Achievement.objects.create(
            title='Released production features',
            metric='12+',
            description='Delivered backend features with deployment automation.',
            sort_order=1,
        )
        Project.objects.create(
            title='Resume Site',
            summary='Created a personal resume site with editable content.',
            tech_stack='Django, SQLite, Pillow',
            result='Live',
            project_url='https://example.com',
            github_url='https://github.com/example/resume',
            sort_order=1,
        )
        SocialLink.objects.create(
            label='GitHub',
            url='https://github.com/example',
            handle='@example',
            sort_order=1,
        )

    def test_home_contains_pdf_download_link(self):
        response = self.client.get(reverse('resume:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('resume:download_pdf'))

    def test_download_route_returns_pdf_attachment(self):
        response = self.client.get(reverse('resume:download_pdf'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment;', response['Content-Disposition'])
        self.assertIn('maxim-roslyakov-resume.pdf', response['Content-Disposition'])
        self.assertTrue(response.content.startswith(b'%PDF'))
        self.assertGreater(len(response.content), 1000)
