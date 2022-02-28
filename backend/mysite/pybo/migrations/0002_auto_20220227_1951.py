# Generated by Django 3.1.3 on 2022-02-27 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meet',
            name='email',
        ),
        migrations.AddField(
            model_name='action',
            name='user_id',
            field=models.ForeignKey(db_column='id', default=1, on_delete=django.db.models.deletion.CASCADE, to='pybo.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agenda',
            name='user_id',
            field=models.ForeignKey(db_column='id', default=1, on_delete=django.db.models.deletion.CASCADE, to='pybo.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meet',
            name='user_id',
            field=models.ForeignKey(db_column='id', default=1, on_delete=django.db.models.deletion.CASCADE, to='pybo.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meet',
            name='goal',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='meet_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='meet_status',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='meet_title',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='participants',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='meet',
            name='rm_status',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='join_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
