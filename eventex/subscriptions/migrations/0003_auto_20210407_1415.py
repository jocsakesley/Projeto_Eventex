# Generated by Django 3.1.2 on 2021-04-07 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20201121_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='nome',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='telefone',
            new_name='phone',
        ),
    ]
