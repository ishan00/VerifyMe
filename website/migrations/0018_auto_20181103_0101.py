# Generated by Django 2.1.2 on 2018-11-03 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_auto_20181102_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='status',
            field=models.CharField(choices=[('N', 'None'), ('F', 'Freeze'), ('P', 'Pending'), ('V', 'Verified'), ('R', 'Rejected')], default='P', max_length=1),
        ),
    ]