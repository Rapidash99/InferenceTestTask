# Generated by Django 3.0.5 on 2020-04-25 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_auto_20200426_0105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='sent',
            new_name='date_sent',
        ),
    ]
