# Generated by Django 4.0.5 on 2022-06-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_siteuser_activation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='activation_code',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
