# Generated by Django 3.1.3 on 2022-03-07 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0013_auto_20220304_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='dead_line',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
