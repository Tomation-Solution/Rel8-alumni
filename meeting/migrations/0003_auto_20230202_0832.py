# Generated by Django 3.2.13 on 2023-02-02 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0002_auto_20230202_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='organiserDetails',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AddField(
            model_name='meeting',
            name='organiserName',
            field=models.CharField(default='', max_length=400),
        ),
    ]
