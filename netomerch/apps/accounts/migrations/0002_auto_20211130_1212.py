# Generated by Django 3.2.8 on 2021-11-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_registered',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='uid',
        ),
        migrations.AddField(
            model_name='customer',
            name='role',
            field=models.CharField(choices=[('MANAGER', 'Manager'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=10, verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
