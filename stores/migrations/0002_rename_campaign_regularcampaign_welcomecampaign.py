# Generated by Django 4.1.5 on 2023-02-21 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Campaign',
            new_name='RegularCampaign',
        ),
        migrations.CreateModel(
            name='WelcomeCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('reward_id', models.CharField(max_length=100)),
                ('reward_name', models.CharField(max_length=100)),
                ('reward_qty', models.IntegerField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]