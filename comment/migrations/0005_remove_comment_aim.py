# Generated by Django 4.2 on 2024-09-20 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_alter_comment_aim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='aim',
        ),
    ]
