# Generated by Django 2.1.1 on 2018-11-27 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
