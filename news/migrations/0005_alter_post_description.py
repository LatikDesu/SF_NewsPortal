# Generated by Django 4.1.7 on 2023-04-23 10:59

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_comment_parent_alter_comment_post_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
