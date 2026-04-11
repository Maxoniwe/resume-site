from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    sort_order = models.PositiveIntegerField(default=10)

    class Meta:
        abstract = True
        ordering = ('sort_order', 'id')


class ResumeProfile(TimestampedModel):
    welcome_text = models.CharField(max_length=80, default='Добро пожаловать')
    resume_title = models.CharField(max_length=120, default='Мое резюме')
    intro_badge = models.CharField(
        max_length=120,
        default='Дизайн / Разработка / Продуктовый подход',
        help_text='Короткая строка над главным заголовком.',
    )
    full_name = models.CharField(max_length=120, default='Твое имя')
    job_title = models.CharField(max_length=140, default='Разработчик и дизайнер')
    availability_note = models.CharField(
        max_length=140,
        default='Открыт к проектам, стажировкам и предложениям о сотрудничестве.',
    )
    hero_summary = models.TextField(
        default=(
            'Создаю аккуратные цифровые продукты, понятные интерфейсы и '
            'проекты, которые не стыдно показать в портфолио.'
        )
    )
    about_title = models.CharField(max_length=80, default='Обо мне')
    about_text = models.TextField(
        default=(
            'В этом блоке можно рассказать о себе, своем опыте, интересах '
            'и о том, что делает твой подход особенным.'
        )
    )
    skills_title = models.CharField(max_length=80, default='Ключевые навыки')
    experience_title = models.CharField(max_length=80, default='Опыт')
    projects_title = models.CharField(max_length=80, default='Проекты')
    achievements_title = models.CharField(max_length=80, default='Достижения')
    contact_title = models.CharField(max_length=80, default='Связаться со мной')
    contact_note = models.CharField(
        max_length=180,
        default='Укажи свои контакты, чтобы с тобой было легко связаться.',
    )
    primary_button_text = models.CharField(max_length=40, default='Написать мне')
    download_button_text = models.CharField(max_length=40, default='Скачать CV')
    profile_photo = models.ImageField(upload_to='profile/', blank=True)
    cv_file = models.FileField(upload_to='cv/', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'Resume profile'
        verbose_name_plural = 'Resume profile'

    def __str__(self):
        return self.full_name

    @property
    def initials(self):
        parts = [chunk.strip() for chunk in self.full_name.split() if chunk.strip()]
        if not parts:
            return 'YN'
        initials = ''.join(piece[0] for piece in parts[:2]).upper()
        return initials


class Skill(TimestampedModel, OrderedModel):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)
    icon_label = models.CharField(
        max_length=6,
        default='DEV',
        help_text='Short label inside the icon circle, for example DEV or UI.',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.title


class Experience(TimestampedModel, OrderedModel):
    role = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    period = models.CharField(max_length=80, help_text='For example: 2023 - Present')
    location = models.CharField(max_length=120, blank=True)
    summary = models.TextField()
    highlights = models.TextField(
        blank=True,
        help_text='Optional bullet-style notes. Put each note on a new line.',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'

    def __str__(self):
        return f'{self.role} at {self.company}'

    @property
    def highlight_items(self):
        return [item.strip() for item in self.highlights.splitlines() if item.strip()]


class Project(TimestampedModel, OrderedModel):
    title = models.CharField(max_length=120)
    summary = models.TextField()
    tech_stack = models.CharField(
        max_length=180,
        blank=True,
        help_text='Comma-separated stack, for example Django, PostgreSQL, Figma.',
    )
    result = models.CharField(
        max_length=120,
        blank=True,
        help_text="Optional short outcome like 'Launched in 3 weeks'.",
    )
    image = models.ImageField(upload_to='projects/', blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    @property
    def stack_items(self):
        return [item.strip() for item in self.tech_stack.split(',') if item.strip()]

    @property
    def monogram(self):
        parts = [chunk.strip() for chunk in self.title.split() if chunk.strip()]
        if not parts:
            return 'PR'
        letters = ''.join(piece[0] for piece in parts[:2]).upper()
        return letters


class Achievement(TimestampedModel, OrderedModel):
    title = models.CharField(max_length=120)
    metric = models.CharField(
        max_length=60,
        blank=True,
        help_text='Optional standout number, for example 12 launches.',
    )
    description = models.TextField()

    class Meta(OrderedModel.Meta):
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'

    def __str__(self):
        return self.title


class SocialLink(TimestampedModel, OrderedModel):
    label = models.CharField(max_length=60)
    url = models.URLField()
    handle = models.CharField(max_length=80, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Social link'
        verbose_name_plural = 'Social links'

    def __str__(self):
        return self.label
