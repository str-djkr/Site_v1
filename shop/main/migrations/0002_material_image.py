# Generated by Django 4.1.2 on 2023-06-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='image',
            field=models.ImageField(default='product_images/Screenshot_1.png', upload_to='product_images_material'),
        ),
    ]
