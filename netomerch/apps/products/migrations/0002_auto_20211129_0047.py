# Generated by Django 3.2.8 on 2021-11-28 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemproperty',
            name='type',
            field=models.CharField(choices=[('TEXT', 'Text'), ('NUMB', 'Number'), ('BOOL', 'Boolean')], default='TEXT', max_length=4, verbose_name='type'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='Anonymous', max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField(default='')),
                ('is_published', models.BooleanField(default=False)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.item')),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
    ]
