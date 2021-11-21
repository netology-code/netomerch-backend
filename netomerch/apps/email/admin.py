from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from apps.email.models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(SummernoteModelAdmin):
    model = EmailTemplate
    summernote_fields = 'template'
    list_display = (
        "id",
        "description",
    )
