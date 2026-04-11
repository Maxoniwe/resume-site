from django.contrib import admin

from .models import Achievement, Experience, Project, ResumeProfile, Skill, SocialLink


@admin.register(ResumeProfile)
class ResumeProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (
            'Hero',
            {
                'fields': (
                    'welcome_text',
                    'resume_title',
                    'intro_badge',
                    'full_name',
                    'job_title',
                    'availability_note',
                    'hero_summary',
                )
            },
        ),
        (
            'Sections',
            {
                'fields': (
                    'about_title',
                    'about_text',
                    'skills_title',
                    'experience_title',
                    'projects_title',
                    'achievements_title',
                    'contact_title',
                    'contact_note',
                )
            },
        ),
        (
            'Actions and contact',
            {
                'fields': (
                    'primary_button_text',
                    'download_button_text',
                    'email',
                    'phone',
                    'location',
                    'profile_photo',
                    'cv_file',
                )
            },
        ),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def has_add_permission(self, request):
        if ResumeProfile.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order', 'icon_label', 'updated_at')
    list_editable = ('sort_order',)
    search_fields = ('title', 'description')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'sort_order', 'company', 'period')
    list_editable = ('sort_order',)
    search_fields = ('role', 'company', 'summary')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order', 'result', 'updated_at')
    list_editable = ('sort_order',)
    search_fields = ('title', 'summary', 'tech_stack')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order', 'metric', 'updated_at')
    list_editable = ('sort_order',)
    search_fields = ('title', 'description', 'metric')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'sort_order', 'handle', 'url')
    list_editable = ('sort_order',)
    search_fields = ('label', 'handle', 'url')


admin.site.site_header = 'Resume site admin'
admin.site.site_title = 'Resume admin'
admin.site.index_title = 'Content management'
