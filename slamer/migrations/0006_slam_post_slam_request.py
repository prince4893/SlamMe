# Generated by Django 3.0.2 on 2020-03-30 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slamer', '0005_user_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='slam_post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_from', models.CharField(max_length=40)),
                ('post_for', models.CharField(max_length=40)),
                ('public', models.BooleanField(null=True)),
                ('f1', models.CharField(max_length=400, null=True)),
                ('f2', models.CharField(max_length=400, null=True)),
                ('f3', models.CharField(max_length=400, null=True)),
                ('f4', models.CharField(max_length=400, null=True)),
                ('f5', models.CharField(max_length=400, null=True)),
                ('f6', models.CharField(max_length=400, null=True)),
                ('f7', models.CharField(max_length=400, null=True)),
                ('f8', models.CharField(max_length=400, null=True)),
                ('f9', models.CharField(max_length=400, null=True)),
                ('f10', models.CharField(max_length=400, null=True)),
                ('f11', models.CharField(max_length=400, null=True)),
                ('f12', models.CharField(max_length=400, null=True)),
                ('f13', models.CharField(max_length=400, null=True)),
                ('f14', models.CharField(max_length=400, null=True)),
                ('f15', models.CharField(max_length=400, null=True)),
                ('f16', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='slam_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_from', models.CharField(max_length=40)),
                ('req_to', models.CharField(max_length=40)),
            ],
        ),
    ]
