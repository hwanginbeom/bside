# Generated by Django 3.1.3 on 2022-03-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0010_auto_20220301_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secession',
            name='reg_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]