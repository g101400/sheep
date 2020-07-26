# Generated by Django 2.2.14 on 2020-07-26 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0004_collect_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectcategory',
            options={'ordering': ('is_show', '-created_time'), 'verbose_name': '用户收藏帖子类别表', 'verbose_name_plural': '用户收藏帖子类别表'},
        ),
        migrations.RemoveField(
            model_name='collectcategory',
            name='resource_num',
        ),
        migrations.AddField(
            model_name='collectcategory',
            name='image',
            field=models.URLField(default=1, verbose_name='收藏类别封面'),
            preserve_default=False,
        ),
    ]