# Generated by Django 2.1.1 on 2018-09-23 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20180923_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_in_list', models.IntegerField(default=0, editable=False)),
                ('point_type', models.CharField(choices=[('N', 'None'), ('F', 'Freeze'), ('P', 'Pending'), ('V', 'Verified'), ('R', 'Rejected')], default='N', editable=False, max_length=1)),
                ('point_comment', models.TextField(editable=False, null=True)),
                ('timestamp', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('resume_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Resume')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=50)),
                ('department', models.CharField(choices=[('CS', 'Computer Science and Engineering'), ('MA', 'Mathematics'), ('EE', 'Electrical Engineering'), ('CE', 'Civil Engineering')], max_length=2)),
                ('year', models.CharField(choices=[('B1', 'B.Tech. 1st Year'), ('B2', 'B.Tech. 2nd Year'), ('B3', 'B.Tech. 3rd Year'), ('B4', 'B.Tech. 4th Year'), ('M1', 'M.Tech. 1st Year'), ('M2', 'M.Tech. 2nd Year')], max_length=2)),
                ('privilege', models.BooleanField(default=False, editable=False)),
                ('position', models.CharField(default='', editable=False, max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Users'),
        ),
        migrations.AddField(
            model_name='point',
            name='resume_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Resume'),
        ),
        migrations.AddField(
            model_name='point',
            name='section_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Section'),
        ),
        migrations.AddField(
            model_name='point',
            name='user_verify',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Users'),
        ),
    ]
