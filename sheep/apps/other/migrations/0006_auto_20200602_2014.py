# Generated by Django 2.2.7 on 2020-06-02 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0005_auto_20200602_1931'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set(),
        ),
    ]