# Generated by Django 2.2.7 on 2020-04-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20191219_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='post',
            name='not_reply',
        ),
        migrations.AddField(
            model_name='post',
            name='content_type',
            field=models.SmallIntegerField(choices=[(1, '富文本'), (2, 'markdown')], default=1, verbose_name='内容类型'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.URLField(null=True, verbose_name='帖子封面'),
        ),
    ]
