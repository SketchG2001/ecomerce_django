# Generated by Django 5.0.2 on 2024-03-03 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
