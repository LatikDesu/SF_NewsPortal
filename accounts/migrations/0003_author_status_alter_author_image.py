# Generated by Django 4.1.7 on 2023-04-24 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_author_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='status',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, default='/static/images/default_avatar.jpg', null=True, upload_to='users_images'),
        ),
    ]
