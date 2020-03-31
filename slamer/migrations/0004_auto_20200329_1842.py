# Generated by Django 3.0.2 on 2020-03-29 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slamer', '0003_user_logged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='key',
        ),
        migrations.RemoveField(
            model_name='user',
            name='logged',
        ),
        migrations.CreateModel(
            name='abs_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('logged', models.BooleanField(null=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slamer.user')),
            ],
        ),
    ]
