# Generated by Django 4.2.7 on 2023-12-20 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcapi', '0002_users_is_superuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datacentercreations',
            options={'managed': False},
        ),
    ]