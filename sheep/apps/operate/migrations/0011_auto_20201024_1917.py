# Generated by Django 2.2.14 on 2020-10-24 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0010_auto_20201020_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='focus',
            name='user_id',
            field=models.PositiveIntegerField(verbose_name='用户'),
        ),
        migrations.AlterUniqueTogether(
            name='focus',
            unique_together={('user_id', 'focus_id')},
        ),
    ]
