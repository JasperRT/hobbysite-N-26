# Generated by Django 5.0.3 on 2024-05-14 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='owner',
            new_name='author',
        ),
    ]
