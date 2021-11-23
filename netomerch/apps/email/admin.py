from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from apps.email.models import EmailTemplate, EmailReceivers


@admin.register(EmailTemplate)
class EmailTemplateAdmin(SummernoteModelAdmin):
    model = EmailTemplate
    summernote_fields = 'template'
    list_display = (
        "id",
        "description",
    )


@admin.register(EmailReceivers)
class EmailReceivers(admin.ModelAdmin):
    model = EmailReceivers
    list_display = (
        "id",
        "description",
    )
