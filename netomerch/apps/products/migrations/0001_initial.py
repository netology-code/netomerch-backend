# Generated by Django 3.2.8 on 2021-12-17 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
            ],
            options={
                'verbose_name': 'Классификатор категории',
                'verbose_name_plural': 'Классификатор категорий',
            },
        ),
        migrations.CreateModel(
            name='DictImageColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='цвет')),
                ('name_eng', models.CharField(max_length=20, null=True, verbose_name='цвет по-английски')),
                ('color_code', models.CharField(default='#000000', max_length=7, verbose_name='код цвета')),
            ],
            options={
                'verbose_name': 'Классификатор цвета',
                'verbose_name_plural': 'Классификатор цветов',
            },
        ),
        migrations.CreateModel(
            name='ImageColorItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='item')),
                ('is_main_color', models.BooleanField(default=False, verbose_name='основной цвет')),
                ('is_main_image', models.BooleanField(default=False, verbose_name='основная картинка')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='oncolor', to='products.dictimagecolor')),
            ],
            options={
                'verbose_name': 'Изображение цвета товара',
                'verbose_name_plural': 'Изображения цвета товара',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Классификатор размера',
                'verbose_name_plural': 'Классификатор размеров',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Классификатор специализации',
                'verbose_name_plural': 'Классификатор специализаций',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('short_description', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=13)),
                ('is_published', models.BooleanField(default=True)),
                ('is_hit', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item', to='products.category')),
                ('imagecolor', models.ManyToManyField(related_name='itemimagecolor', through='products.ImageColorItem', to='products.DictImageColor')),
                ('size', models.ManyToManyField(related_name='item', to='products.Size')),
                ('specialization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item', to='products.specialization')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.AddField(
            model_name='imagecoloritem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='onitem', to='products.item'),
        ),
    ]
