# Generated by Django 4.1.1 on 2022-10-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_options_post_created_post_publish_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='some post', max_length=250, unique=True),
        ),
    ]
