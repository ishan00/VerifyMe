# Generated by Django 2.1.2 on 2018-10-14 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20181014_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='resume_id',
        ),
    ]