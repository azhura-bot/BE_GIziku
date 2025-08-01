# Generated by Django 5.2.4 on 2025-07-25 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('photo_food', models.ImageField(blank=True, null=True, upload_to='images/food/')),
                ('category', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('nutrition', models.IntegerField()),
                ('cook_time', models.IntegerField()),
                ('preparation_time', models.IntegerField()),
                ('instruction', models.TextField()),
                ('ingridients', models.TextField()),
            ],
        ),
    ]
