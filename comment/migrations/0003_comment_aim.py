# Generated by Django 4.2 on 2024-09-18 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_pv_post_uv'),
        ('comment', '0002_alter_comment_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='aim',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='存储目标'),
            preserve_default=False,
        ),
    ]
