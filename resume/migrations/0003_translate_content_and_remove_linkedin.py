from django.db import migrations


def apply_updates(apps, schema_editor):
    ResumeProfile = apps.get_model('resume', 'ResumeProfile')
    Skill = apps.get_model('resume', 'Skill')
    Experience = apps.get_model('resume', 'Experience')
    Project = apps.get_model('resume', 'Project')
    Achievement = apps.get_model('resume', 'Achievement')
    SocialLink = apps.get_model('resume', 'SocialLink')

    profile = ResumeProfile.objects.first()
    if profile:
        profile.welcome_text = 'Добро пожаловать'
        profile.resume_title = 'Мое резюме'
        profile.intro_badge = 'Django / UI / Продуктовый подход'
        profile.full_name = 'Твое имя'
        profile.job_title = 'Full-stack разработчик и дизайнер'
        profile.availability_note = 'Открыт к фрилансу, стажировкам и предложениям о сотрудничестве.'
        profile.hero_summary = 'Замени этот стартовый текст на свою историю, сильные стороны, цели и проекты, которые хочешь показывать работодателям или клиентам.'
        profile.about_title = 'Обо мне'
        profile.about_text = 'Здесь можно коротко рассказать о себе, своем бэкграунде, интересах и о том, какую работу тебе нравится делать больше всего.'
        profile.skills_title = 'Ключевые навыки'
        profile.experience_title = 'Опыт'
        profile.projects_title = 'Избранные проекты'
        profile.achievements_title = 'Достижения'
        profile.contact_title = 'Связаться со мной'
        profile.contact_note = 'Весь текст на этой странице можно менять через Django admin.'
        profile.primary_button_text = 'Написать мне'
        profile.download_button_text = 'Скачать CV'
        if profile.location == 'Your City, Country':
            profile.location = 'Твой город, страна'
        profile.save()

    skill_updates = {
        'Web Development': ('Веб-разработка', 'Создание лендингов, дашбордов и полноценных веб-продуктов.'),
        'UI and UX': ('UI и UX', 'Создание интерфейсов с хорошей иерархией, отступами и понятной структурой.'),
        'Brand Systems': ('Визуальные системы', 'Помогаю превращать сырые идеи в аккуратное и цельное оформление.'),
        'SEO and Content': ('SEO и контент', 'Структурирую страницы так, чтобы их было приятно читать и легко находить.'),
    }
    for skill in Skill.objects.all():
        if skill.title in skill_updates:
            skill.title, skill.description = skill_updates[skill.title]
            skill.save()

    experience_updates = {
        'Frontend Developer': {
            'role': 'Frontend разработчик',
            'period': '2024 - настоящее время',
            'location': 'Удаленно',
            'summary': 'Проектировал и запускал клиентские страницы с упором на аккуратные интерфейсы и адаптивность.',
            'highlights': 'Собрал переиспользуемые UI-блоки для ускорения запусков.\nТесно работал с дизайном, чтобы доводить детали до релиза.',
        },
        'Freelance Designer': {
            'role': 'Фриланс дизайнер',
            'company': 'Независимые проекты',
            'location': 'Гибрид',
            'summary': 'Помогал небольшим брендам и авторам оформлять свое присутствие в интернете через лендинги и портфолио-сайты.',
            'highlights': 'Вел и визуальное направление, и реализацию.\nДелал сайты, которые заказчики могли потом редактировать сами.',
        },
    }
    for exp in Experience.objects.all():
        if exp.role in experience_updates:
            for field, value in experience_updates[exp.role].items():
                setattr(exp, field, value)
            exp.save()

    project_updates = {
        'Portfolio Platform': {
            'title': 'Платформа-портфолио',
            'summary': 'Персональный сайт с редактируемыми блоками, плавной структурой и загрузкой медиа.',
            'result': 'Редактируемый сайт',
        },
        'Product Launch Page': {
            'title': 'Страница запуска продукта',
            'summary': 'Промо-страница для стартапа с акцентом на визуальную подачу и конверсию.',
            'result': 'Запуск за 3 недели',
        },
        'Creator Media Kit': {
            'title': 'Медиа-кит автора',
            'summary': 'Презентационный сайт для сотрудничества, демонстрации кейсов и удобного контакта.',
            'result': 'Обновление бренда',
        },
    }
    for project in Project.objects.all():
        if project.title in project_updates:
            for field, value in project_updates[project.title].items():
                setattr(project, field, value)
            project.save()

    achievement_updates = {
        'Project Delivery': ('Запуск проектов', '12+ релизов', 'Запустил несколько личных и клиентских проектов, сохраняя баланс между скоростью и качеством подачи.'),
        'Design to Code': ('От дизайна до кода', 'Полный цикл', 'Доводил проекты от идеи и визуала до рабочей реализации без лишних передач между командами.'),
        'Editable Content': ('Редактируемый контент', 'Admin-ready', 'Делал сайты, которые легко обновлять после запуска, а не одноразовые статичные страницы.'),
    }
    for achievement in Achievement.objects.all():
        if achievement.title in achievement_updates:
            achievement.title, achievement.metric, achievement.description = achievement_updates[achievement.title]
            achievement.save()

    SocialLink.objects.filter(label='LinkedIn').delete()


def revert_updates(apps, schema_editor):
    SocialLink = apps.get_model('resume', 'SocialLink')
    if not SocialLink.objects.filter(label='LinkedIn').exists():
        SocialLink.objects.create(
            sort_order=20,
            label='LinkedIn',
            handle='linkedin.com/in/yourname',
            url='https://linkedin.com',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_seed_demo_content'),
    ]

    operations = [
        migrations.RunPython(apply_updates, revert_updates),
    ]
