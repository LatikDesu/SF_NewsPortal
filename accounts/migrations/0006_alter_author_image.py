# Generated by Django 4.1.7 on 2023-04-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_author_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, default='users_images/default_avatar.jpg', null=True, upload_to='users_images'),
        ),
    ]
