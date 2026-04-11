from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PAGE_WIDTH = 1240
PAGE_HEIGHT = 1754
PAGE_SIZE = (PAGE_WIDTH, PAGE_HEIGHT)
PAGE_MARGIN_X = 90
PAGE_MARGIN_Y = 90
CONTENT_WIDTH = PAGE_WIDTH - (PAGE_MARGIN_X * 2)
CARD_GAP = 28

COLOR_BACKGROUND = "#F7F7F5"
COLOR_SURFACE = "#FFFFFF"
COLOR_SURFACE_ALT = "#EEF6F3"
COLOR_TEXT = "#182026"
COLOR_MUTED = "#5B6470"
COLOR_ACCENT = "#0F766E"
COLOR_BORDER = "#D5DDD8"


def build_resume_pdf(profile, skills, experiences, projects, achievements, social_links):
    builder = ResumePdfBuilder(
        profile=profile,
        skills=list(skills),
        experiences=list(experiences),
        projects=list(projects),
        achievements=list(achievements),
        social_links=list(social_links),
    )
    return builder.build()


class ResumePdfBuilder:
    def __init__(self, profile, skills, experiences, projects, achievements, social_links):
        self.profile = profile
        self.skills = skills
        self.experiences = experiences
        self.projects = projects
        self.achievements = achievements
        self.social_links = social_links

        self.fonts = {
            "title": self._load_font(52, bold=True),
            "subtitle": self._load_font(30, bold=True),
            "section": self._load_font(28, bold=True),
            "card_title": self._load_font(22, bold=True),
            "body": self._load_font(18),
            "body_bold": self._load_font(18, bold=True),
            "small": self._load_font(15),
            "small_bold": self._load_font(15, bold=True),
        }

        self.pages = []
        self.page_number = 0
        self.page = None
        self.draw = None
        self.y = PAGE_MARGIN_Y

    def build(self):
        self._new_page()
        self._draw_cover()
        self._draw_about()
        self._draw_social_links()
        self._draw_skills()
        self._draw_experience()
        self._draw_achievements()
        self._draw_projects()
        self._draw_contacts()

        if self.page is not None:
            self.pages.append(self.page)

        self._draw_page_footers()

        buffer = BytesIO()
        pdf_pages = [page.convert("RGB") for page in self.pages]
        pdf_pages[0].save(
            buffer,
            format="PDF",
            save_all=True,
            append_images=pdf_pages[1:],
            resolution=150.0,
        )
        return buffer.getvalue()

    def _new_page(self):
        if self.page is not None:
            self.pages.append(self.page)

        self.page_number += 1
        self.page = Image.new("RGB", PAGE_SIZE, COLOR_BACKGROUND)
        self.draw = ImageDraw.Draw(self.page)
        self.y = PAGE_MARGIN_Y

        self._draw_page_background()
        if self.page_number > 1:
            self._draw_running_header()

    def _draw_page_background(self):
        self.draw.rounded_rectangle(
            [
                PAGE_MARGIN_X - 24,
                PAGE_MARGIN_Y - 24,
                PAGE_WIDTH - PAGE_MARGIN_X + 24,
                PAGE_HEIGHT - PAGE_MARGIN_Y + 24,
            ],
            radius=36,
            fill=COLOR_SURFACE,
            outline=COLOR_BORDER,
            width=2,
        )

    def _draw_running_header(self):
        header_text = self.profile.full_name or self.profile.resume_title or "Resume"
        self.draw.text(
            (PAGE_MARGIN_X, self.y),
            header_text,
            font=self.fonts["small_bold"],
            fill=COLOR_MUTED,
        )
        self.draw.line(
            (
                PAGE_MARGIN_X,
                self.y + 34,
                PAGE_WIDTH - PAGE_MARGIN_X,
                self.y + 34,
            ),
            fill=COLOR_BORDER,
            width=2,
        )
        self.y += 58

    def _draw_cover(self):
        photo_size = 210
        right_x = PAGE_WIDTH - PAGE_MARGIN_X - photo_size
        left_width = CONTENT_WIDTH - photo_size - 40
        photo_bottom = self.y

        badge = self._clean_text(self.profile.intro_badge)
        if badge:
            self.draw.rounded_rectangle(
                [PAGE_MARGIN_X, self.y, PAGE_MARGIN_X + 380, self.y + 40],
                radius=20,
                fill=COLOR_SURFACE_ALT,
            )
            self.draw.text(
                (PAGE_MARGIN_X + 16, self.y + 9),
                badge,
                font=self.fonts["small_bold"],
                fill=COLOR_ACCENT,
            )
            self.y += 58

        if self.profile.profile_photo:
            photo_bounds = [right_x, self.y - 12, right_x + photo_size, self.y - 12 + photo_size]
            self._draw_photo(photo_bounds)
            photo_bottom = photo_bounds[3] + 28

        self.draw.text(
            (PAGE_MARGIN_X, self.y),
            self.profile.full_name or "Resume",
            font=self.fonts["title"],
            fill=COLOR_TEXT,
        )
        self.y += self._line_height(self.fonts["title"]) + 8

        job_title = self._clean_text(self.profile.job_title)
        if job_title:
            self.draw.text(
                (PAGE_MARGIN_X, self.y),
                job_title,
                font=self.fonts["subtitle"],
                fill=COLOR_ACCENT,
            )
            self.y += self._line_height(self.fonts["subtitle"]) + 16

        if self._clean_text(self.profile.resume_title):
            self.y = self._draw_wrapped_text(
                PAGE_MARGIN_X,
                self.y,
                self.profile.resume_title,
                self.fonts["body_bold"],
                left_width,
                fill=COLOR_TEXT,
                line_spacing=6,
            )
            self.y += 10

        if self._clean_text(self.profile.hero_summary):
            self.y = self._draw_wrapped_text(
                PAGE_MARGIN_X,
                self.y,
                self.profile.hero_summary,
                self.fonts["body"],
                left_width,
                fill=COLOR_MUTED,
                line_spacing=8,
            )

        self.y += 18

        top_card_y = self.y
        contact_lines = self._contact_lines()
        if contact_lines:
            card_height = max(110, 34 + len(contact_lines) * 34)
            self.draw.rounded_rectangle(
                [PAGE_MARGIN_X, top_card_y, PAGE_WIDTH - PAGE_MARGIN_X, top_card_y + card_height],
                radius=28,
                fill=COLOR_SURFACE_ALT,
            )
            self.draw.text(
                (PAGE_MARGIN_X + 24, top_card_y + 20),
                "Контакты",
                font=self.fonts["small_bold"],
                fill=COLOR_ACCENT,
            )
            current_y = top_card_y + 54
            for line in contact_lines:
                self.draw.text(
                    (PAGE_MARGIN_X + 24, current_y),
                    line,
                    font=self.fonts["body"],
                    fill=COLOR_TEXT,
                )
                current_y += 30
            self.y = top_card_y + card_height + 28

        self.y = max(self.y, photo_bottom)

    def _draw_about(self):
        about_text = self._clean_text(self.profile.about_text)
        if not about_text:
            return

        self._draw_section_heading(self.profile.about_title or "Обо мне")
        self.y = self._draw_wrapped_text(
            PAGE_MARGIN_X,
            self.y,
            about_text,
            self.fonts["body"],
            CONTENT_WIDTH,
            fill=COLOR_TEXT,
            line_spacing=10,
        )
        self.y += 20

    def _draw_social_links(self):
        if not self.social_links:
            return

        lines = []
        for link in self.social_links:
            parts = [self._clean_text(link.label), self._clean_text(link.handle), self._clean_text(link.url)]
            line = " • ".join(part for part in parts if part)
            if line:
                lines.append(line)

        if not lines:
            return

        self._draw_section_heading("Онлайн")
        for line in lines:
            self.y = self._draw_bullet_line(line)
        self.y += 18

    def _draw_skills(self):
        if not self.skills:
            return

        self._draw_section_heading(self.profile.skills_title or "Навыки")
        for skill in self.skills:
            body = self._clean_text(skill.description)
            title = self._clean_text(skill.title)
            line = f"{title}: {body}" if body else title
            self.y = self._draw_bullet_line(line)
        self.y += 18

    def _draw_experience(self):
        if not self.experiences:
            return

        self._draw_section_heading(self.profile.experience_title or "Опыт")
        for experience in self.experiences:
            highlights = getattr(experience, "highlight_items", [])
            summary_lines = self._wrap_text(self._clean_text(experience.summary), self.fonts["body"], CONTENT_WIDTH - 40)
            block_height = 80 + len(summary_lines) * 28 + len(highlights) * 28
            self._ensure_space(block_height)

            start_y = self.y
            self.draw.rounded_rectangle(
                [PAGE_MARGIN_X, start_y, PAGE_WIDTH - PAGE_MARGIN_X, start_y + block_height],
                radius=26,
                fill=COLOR_SURFACE_ALT,
            )
            title = self._clean_text(experience.role)
            company = self._clean_text(experience.company)
            heading = " @ ".join(part for part in [title, company] if part)
            self.draw.text(
                (PAGE_MARGIN_X + 24, start_y + 20),
                heading,
                font=self.fonts["card_title"],
                fill=COLOR_TEXT,
            )

            badges = " • ".join(
                part
                for part in [self._clean_text(experience.period), self._clean_text(experience.location)]
                if part
            )
            if badges:
                self.draw.text(
                    (PAGE_MARGIN_X + 24, start_y + 54),
                    badges,
                    font=self.fonts["small_bold"],
                    fill=COLOR_ACCENT,
                )

            current_y = start_y + 86
            current_y = self._draw_wrapped_text(
                PAGE_MARGIN_X + 24,
                current_y,
                experience.summary,
                self.fonts["body"],
                CONTENT_WIDTH - 48,
                fill=COLOR_TEXT,
                line_spacing=8,
            )

            for item in highlights:
                current_y = self._draw_bullet_line(
                    item,
                    y=current_y,
                    x=PAGE_MARGIN_X + 24,
                    max_width=CONTENT_WIDTH - 48,
                    bullet_fill=COLOR_ACCENT,
                )

            self.y = start_y + block_height + CARD_GAP

    def _draw_achievements(self):
        if not self.achievements:
            return

        self._draw_section_heading(self.profile.achievements_title or "Достижения")
        for achievement in self.achievements:
            parts = [self._clean_text(achievement.metric), self._clean_text(achievement.title)]
            heading = " • ".join(part for part in parts if part)
            if heading:
                self.y = self._draw_bullet_line(heading, bullet_fill=COLOR_ACCENT, text_font=self.fonts["body_bold"])
            description = self._clean_text(achievement.description)
            if description:
                self.y = self._draw_wrapped_text(
                    PAGE_MARGIN_X + 22,
                    self.y - 4,
                    description,
                    self.fonts["body"],
                    CONTENT_WIDTH - 22,
                    fill=COLOR_MUTED,
                    line_spacing=8,
                )
                self.y += 10
        self.y += 8

    def _draw_projects(self):
        if not self.projects:
            return

        self._draw_section_heading(self.profile.projects_title or "Проекты")
        for project in self.projects:
            stack = ", ".join(getattr(project, "stack_items", []))
            links = " | ".join(
                part
                for part in [self._clean_text(project.project_url), self._clean_text(project.github_url)]
                if part
            )
            summary = self._clean_text(project.summary)
            lines = [summary]
            if stack:
                lines.append(f"Стек: {stack}")
            if links:
                lines.append(f"Ссылки: {links}")

            wrapped_line_count = sum(
                len(self._wrap_text(line, self.fonts["body"], CONTENT_WIDTH - 48))
                for line in lines
                if line
            )
            block_height = 74 + (wrapped_line_count * 28)
            self._ensure_space(block_height)

            start_y = self.y
            self.draw.rounded_rectangle(
                [PAGE_MARGIN_X, start_y, PAGE_WIDTH - PAGE_MARGIN_X, start_y + block_height],
                radius=26,
                outline=COLOR_BORDER,
                width=2,
                fill=COLOR_SURFACE,
            )

            title = self._clean_text(project.title)
            if self._clean_text(project.result):
                title = f"{title} ({project.result})"
            self.draw.text(
                (PAGE_MARGIN_X + 24, start_y + 20),
                title,
                font=self.fonts["card_title"],
                fill=COLOR_TEXT,
            )

            current_y = start_y + 58
            for line in lines:
                if not line:
                    continue
                current_y = self._draw_wrapped_text(
                    PAGE_MARGIN_X + 24,
                    current_y,
                    line,
                    self.fonts["body"],
                    CONTENT_WIDTH - 48,
                    fill=COLOR_TEXT if line == summary else COLOR_MUTED,
                    line_spacing=8,
                )
                current_y += 6

            self.y = start_y + block_height + CARD_GAP

    def _draw_contacts(self):
        contact_lines = self._contact_lines()
        if not contact_lines:
            return

        self._draw_section_heading(self.profile.contact_title or "Контакты")
        note = self._clean_text(self.profile.contact_note)
        if note:
            self.y = self._draw_wrapped_text(
                PAGE_MARGIN_X,
                self.y,
                note,
                self.fonts["body"],
                CONTENT_WIDTH,
                fill=COLOR_MUTED,
                line_spacing=8,
            )
            self.y += 10

        for line in contact_lines:
            self.y = self._draw_bullet_line(line)

    def _draw_section_heading(self, title):
        self._ensure_space(78)
        self.draw.text(
            (PAGE_MARGIN_X, self.y),
            self._clean_text(title),
            font=self.fonts["section"],
            fill=COLOR_TEXT,
        )
        line_y = self.y + 38
        self.draw.line(
            (PAGE_MARGIN_X, line_y, PAGE_WIDTH - PAGE_MARGIN_X, line_y),
            fill=COLOR_BORDER,
            width=2,
        )
        self.y += 56

    def _draw_bullet_line(
        self,
        text,
        y=None,
        x=PAGE_MARGIN_X,
        max_width=CONTENT_WIDTH,
        bullet_fill=COLOR_TEXT,
        text_font=None,
    ):
        font = text_font or self.fonts["body"]
        lines = self._wrap_text(self._clean_text(text), font, max_width - 22)
        estimated_height = max(34, len(lines) * (self._line_height(font) + 8))
        current_y = self.y if y is None else y
        if y is None:
            self._ensure_space(estimated_height + 4)
            current_y = self.y
        bullet_y = current_y + 8
        self.draw.ellipse([x, bullet_y, x + 10, bullet_y + 10], fill=bullet_fill)
        new_y = self._draw_wrapped_text(
            x + 20,
            current_y,
            text,
            font,
            max_width - 20,
            fill=COLOR_TEXT,
            line_spacing=8,
        )
        return new_y + 2

    def _draw_wrapped_text(
        self,
        x,
        y,
        text,
        font,
        max_width,
        fill,
        line_spacing=6,
    ):
        lines = self._wrap_text(self._clean_text(text), font, max_width)
        current_y = y
        line_height = self._line_height(font)
        for line in lines:
            if line:
                self.draw.text((x, current_y), line, font=font, fill=fill)
            current_y += line_height + line_spacing
        return current_y

    def _draw_photo(self, bounds):
        try:
            source = Image.open(self.profile.profile_photo.path).convert("RGB")
        except Exception:
            return

        left, top, right, bottom = bounds
        size = (right - left, bottom - top)
        fitted = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS)
        mask = Image.new("L", size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, size[0], size[1]], radius=36, fill=255)
        self.page.paste(fitted, (left, top), mask)
        self.draw.rounded_rectangle(bounds, radius=36, outline=COLOR_BORDER, width=4)

    def _draw_page_footers(self):
        total = len(self.pages)
        for index, page in enumerate(self.pages, start=1):
            footer = ImageDraw.Draw(page)
            footer.line(
                (
                    PAGE_MARGIN_X,
                    PAGE_HEIGHT - PAGE_MARGIN_Y + 10,
                    PAGE_WIDTH - PAGE_MARGIN_X,
                    PAGE_HEIGHT - PAGE_MARGIN_Y + 10,
                ),
                fill=COLOR_BORDER,
                width=2,
            )
            footer.text(
                (PAGE_MARGIN_X, PAGE_HEIGHT - PAGE_MARGIN_Y + 26),
                self.profile.full_name or "Resume",
                font=self.fonts["small"],
                fill=COLOR_MUTED,
            )
            footer.text(
                (PAGE_WIDTH - PAGE_MARGIN_X - 80, PAGE_HEIGHT - PAGE_MARGIN_Y + 26),
                f"{index}/{total}",
                font=self.fonts["small_bold"],
                fill=COLOR_MUTED,
            )

    def _ensure_space(self, required_height):
        if self.y + required_height <= PAGE_HEIGHT - PAGE_MARGIN_Y - 70:
            return
        self._new_page()

    def _contact_lines(self):
        return [
            line
            for line in [
                self._format_contact_line("Email", self.profile.email),
                self._format_contact_line("Телефон", self.profile.phone),
                self._format_contact_line("Локация", self.profile.location),
            ]
            if line
        ]

    def _format_contact_line(self, label, value):
        value = self._clean_text(value)
        if not value:
            return ""
        return f"{label}: {value}"

    def _wrap_text(self, text, font, max_width):
        if not text:
            return []

        wrapped_lines = []
        for paragraph in text.splitlines():
            compact = " ".join(paragraph.split())
            if not compact:
                wrapped_lines.append("")
                continue

            current_line = ""
            for word in compact.split(" "):
                chunks = self._split_long_word(word, font, max_width)
                for index, chunk in enumerate(chunks):
                    separator = " " if current_line and index == 0 else ""
                    candidate = f"{current_line}{separator}{chunk}"
                    if self._text_width(candidate, font) <= max_width:
                        current_line = candidate
                        continue

                    if current_line:
                        wrapped_lines.append(current_line)
                    current_line = chunk

            if current_line:
                wrapped_lines.append(current_line)

        return wrapped_lines

    def _split_long_word(self, word, font, max_width):
        if self._text_width(word, font) <= max_width:
            return [word]

        chunks = []
        current = ""
        for char in word:
            candidate = f"{current}{char}"
            if current and self._text_width(candidate, font) > max_width:
                chunks.append(current)
                current = char
            else:
                current = candidate
        if current:
            chunks.append(current)
        return chunks

    def _text_width(self, text, font):
        if not text:
            return 0
        left, top, right, bottom = self.draw.textbbox((0, 0), text, font=font)
        return right - left

    def _line_height(self, font):
        left, top, right, bottom = self.draw.textbbox((0, 0), "Ag", font=font)
        return bottom - top

    def _load_font(self, size, bold=False):
        font_candidates = self._font_candidates(bold)
        for candidate in font_candidates:
            try:
                if Path(candidate).exists():
                    return ImageFont.truetype(candidate, size=size)
            except OSError:
                continue

        try:
            font_name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
            return ImageFont.truetype(font_name, size=size)
        except OSError:
            return ImageFont.load_default()

    def _font_candidates(self, bold):
        if bold:
            return [
                r"C:\Windows\Fonts\arialbd.ttf",
                r"C:\Windows\Fonts\segoeuib.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]

        return [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]

    def _clean_text(self, value):
        if value is None:
            return ""
        return str(value).strip()
