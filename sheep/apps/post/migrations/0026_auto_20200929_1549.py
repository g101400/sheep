# Generated by Django 2.2.14 on 2020-09-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0025_auto_20200929_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreply',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='是否已读'),
        ),
    ]