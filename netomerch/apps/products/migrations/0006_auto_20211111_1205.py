# Generated by Django 3.2.8 on 2021-11-11 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_category_parent_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='specproperty',
            options={'verbose_name': 'Special property', 'verbose_name_plural': 'Special Properties'},
        ),
    ]