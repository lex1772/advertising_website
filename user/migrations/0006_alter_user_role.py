# Generated by Django 4.2.5 on 2023-09-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=9, null=True),
        ),
    ]
