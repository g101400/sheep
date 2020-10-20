# Generated by Django 2.2.14 on 2020-10-19 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20201019_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, verbose_name='用户名'),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('username', 'is_active')},
        ),
    ]
