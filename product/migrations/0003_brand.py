# Generated by Django 4.1.7 on 2023-04-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_is_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=250, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]