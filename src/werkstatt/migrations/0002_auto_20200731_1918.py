# Generated by Django 3.0.6 on 2020-07-31 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('werkstatt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='notice',
        ),
        migrations.AddField(
            model_name='contact',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
