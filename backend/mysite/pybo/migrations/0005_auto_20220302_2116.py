# Generated by Django 3.1.3 on 2022-03-02 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0004_auto_20220301_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secession',
            name='cause',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='secession',
            name='reg_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='selfcheck',
            name='efficiency',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='selfcheck',
            name='ownership',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='selfcheck',
            name='participation',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='selfcheck',
            name='productivity',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
