# Generated by Django 3.2.8 on 2021-11-08 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='addresses',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]