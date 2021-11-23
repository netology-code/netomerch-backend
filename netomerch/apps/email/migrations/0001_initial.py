# Generated by Django 3.2.8 on 2021-11-23 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('template', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблоны',
            },
        ),
        migrations.CreateModel(
            name='EmailReceivers',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('email_list', models.CharField(max_length=255)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receivers', to='email.emailtemplate')),
            ],
            options={
                'verbose_name': 'Получатели',
                'verbose_name_plural': 'Получатели',
            },
        ),
    ]