# Generated by Django 4.1.5 on 2023-02-21 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]
