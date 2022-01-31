# Generated by Django 3.1.1 on 2022-01-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20220123_2133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='item',
            new_name='action_title',
        ),
        migrations.RenameField(
            model_name='meet',
            old_name='meet_name',
            new_name='meet_title',
        ),
        migrations.AddField(
            model_name='agenda',
            name='agenda_title',
            field=models.TextField(default='', null=True),
        ),
    ]