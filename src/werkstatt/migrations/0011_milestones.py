# Generated by Django 3.1.1 on 2020-09-14 13:55

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('werkstatt', '0010_auto_20200910_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years', models.CharField(max_length=100)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('draft', models.BooleanField(default=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
