from django.db import migrations


def seed_demo_content(apps, schema_editor):
    ResumeProfile = apps.get_model('resume', 'ResumeProfile')
    Skill = apps.get_model('resume', 'Skill')
    Experience = apps.get_model('resume', 'Experience')
    Project = apps.get_model('resume', 'Project')
    Achievement = apps.get_model('resume', 'Achievement')
    SocialLink = apps.get_model('resume', 'SocialLink')

    if not ResumeProfile.objects.exists():
        ResumeProfile.objects.create(
            welcome_text='Добро пожаловать',
            resume_title='Мое резюме',
            intro_badge='Django / UI / Продуктовый подход',
            full_name='Твое имя',
            job_title='Full-stack разработчик и дизайнер',
            availability_note='Открыт к фрилансу, стажировкам и предложениям о сотрудничестве.',
            hero_summary='Замени этот стартовый текст на свою историю, сильные стороны, цели и проекты, которые хочешь показывать работодателям или клиентам.',
            about_title='Обо мне',
            about_text='Здесь можно коротко рассказать о себе, своем бэкграунде, интересах и о том, какую работу тебе нравится делать больше всего.',
            skills_title='Ключевые навыки',
            experience_title='Опыт',
            projects_title='Избранные проекты',
            achievements_title='Достижения',
            contact_title='Связаться со мной',
            contact_note='Весь текст на этой странице можно менять через Django admin.',
            primary_button_text='Написать мне',
            download_button_text='Скачать CV',
            email='hello@example.com',
            phone='+1 234 567 890',
            location='Твой город, страна',
        )

    if not Skill.objects.exists():
        Skill.objects.bulk_create(
            [
                Skill(sort_order=10, title='Web Development', description='Build landing pages, dashboards, and full-stack products.', icon_label='DEV'),
                Skill(sort_order=20, title='UI и UX', description='Создание интерфейсов с хорошей иерархией, отступами и понятной структурой.', icon_label='UI'),
                Skill(sort_order=30, title='Визуальные системы', description='Помогаю превращать сырые идеи в аккуратное и цельное оформление.', icon_label='BR'),
                Skill(sort_order=40, title='SEO и контент', description='Структурирую страницы так, чтобы их было приятно читать и легко находить.', icon_label='SEO'),
            ]
        )

    if not Experience.objects.exists():
        Experience.objects.bulk_create(
            [
                Experience(
                    sort_order=10,
                    role='Frontend разработчик',
                    company='Creative Studio',
                    period='2024 - настоящее время',
                    location='Удаленно',
                    summary='Проектировал и запускал клиентские страницы с упором на аккуратные интерфейсы и адаптивность.',
                    highlights='Собрал переиспользуемые UI-блоки для ускорения запусков.\nТесно работал с дизайном, чтобы доводить детали до релиза.',
                ),
                Experience(
                    sort_order=20,
                    role='Фриланс дизайнер',
                    company='Независимые проекты',
                    period='2022 - 2024',
                    location='Гибрид',
                    summary='Помогал небольшим брендам и авторам оформлять свое присутствие в интернете через лендинги и портфолио-сайты.',
                    highlights='Вел и визуальное направление, и реализацию.\nДелал сайты, которые заказчики могли потом редактировать сами.',
                ),
            ]
        )

    if not Project.objects.exists():
        Project.objects.bulk_create(
            [
                Project(
                    sort_order=10,
                    title='Платформа-портфолио',
                    summary='Персональный сайт с редактируемыми блоками, плавной структурой и загрузкой медиа.',
                    tech_stack='Django, HTML, CSS',
                    result='Редактируемый сайт',
                    project_url='https://example.com',
                    github_url='https://github.com/example/portfolio-platform',
                ),
                Project(
                    sort_order=20,
                    title='Страница запуска продукта',
                    summary='Промо-страница для стартапа с акцентом на визуальную подачу и конверсию.',
                    tech_stack='Django, Figma, Responsive Design',
                    result='Запуск за 3 недели',
                    project_url='https://example.com',
                ),
                Project(
                    sort_order=30,
                    title='Медиа-кит автора',
                    summary='Презентационный сайт для сотрудничества, демонстрации кейсов и удобного контакта.',
                    tech_stack='Django, Content Strategy, UI',
                    result='Обновление бренда',
                    project_url='https://example.com',
                ),
            ]
        )

    if not Achievement.objects.exists():
        Achievement.objects.bulk_create(
            [
                Achievement(sort_order=10, title='Запуск проектов', metric='12+ релизов', description='Запустил несколько личных и клиентских проектов, сохраняя баланс между скоростью и качеством подачи.'),
                Achievement(sort_order=20, title='От дизайна до кода', metric='Полный цикл', description='Доводил проекты от идеи и визуала до рабочей реализации без лишних передач между командами.'),
                Achievement(sort_order=30, title='Редактируемый контент', metric='Admin-ready', description='Делал сайты, которые легко обновлять после запуска, а не одноразовые статичные страницы.'),
            ]
        )

    if not SocialLink.objects.exists():
        SocialLink.objects.bulk_create(
            [
                SocialLink(sort_order=10, label='GitHub', handle='github.com/yourname', url='https://github.com/example'),
                SocialLink(sort_order=20, label='Telegram', handle='t.me/yourname', url='https://t.me'),
            ]
        )


def remove_demo_content(apps, schema_editor):
    ResumeProfile = apps.get_model('resume', 'ResumeProfile')
    Skill = apps.get_model('resume', 'Skill')
    Experience = apps.get_model('resume', 'Experience')
    Project = apps.get_model('resume', 'Project')
    Achievement = apps.get_model('resume', 'Achievement')
    SocialLink = apps.get_model('resume', 'SocialLink')

    SocialLink.objects.all().delete()
    Achievement.objects.all().delete()
    Project.objects.all().delete()
    Experience.objects.all().delete()
    Skill.objects.all().delete()
    ResumeProfile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_content, remove_demo_content),
    ]
