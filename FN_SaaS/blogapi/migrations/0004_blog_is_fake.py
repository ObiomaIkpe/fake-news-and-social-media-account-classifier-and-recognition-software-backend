# Generated by Django 5.1.4 on 2025-01-11 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0003_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_fake',
            field=models.BooleanField(default=False),
        ),
    ]
