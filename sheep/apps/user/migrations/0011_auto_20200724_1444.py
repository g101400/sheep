# Generated by Django 2.2.14 on 2020-07-24 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_last_login_addr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_login_addr',
        ),
        migrations.AddField(
            model_name='user',
            name='last_login_city',
            field=models.CharField(default='', max_length=24, verbose_name='上次登录城市'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login_province',
            field=models.CharField(default='', max_length=12, verbose_name='上次登录省份'),
        ),
    ]
