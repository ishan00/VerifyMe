# Generated by Django 2.1.1 on 2018-11-26 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_auto_20181125_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='type',
            field=models.CharField(choices=[('BU', 'Bullet'), ('BL', 'Block'), ('M', 'Multi')], default='BU', editable=False, max_length=2),
        ),
    ]
