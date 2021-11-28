# Generated by Django 3.2.8 on 2021-11-27 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_itemproperty_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemproperty',
            name='type',
            field=models.CharField(choices=[('TEXT', 'Text'), ('NUMB', 'Number'), ('BOOL', 'Boolean')], default='TEXT', max_length=4, verbose_name='type'),
        ),
    ]
