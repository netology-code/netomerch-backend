from django.contrib import admin

from apps.email.models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate

    list_display = (
        "id",
        "description",
    )
