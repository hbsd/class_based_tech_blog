# Generated by Django 4.1.1 on 2022-10-07 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_title_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title_image',
            field=models.ImageField(default='default_title_image.jpg', upload_to='title_image/'),
        ),
    ]
