# Generated by Django 3.2.13 on 2023-02-13 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postions',
            name='nothing',
            field=models.CharField(blank=True, default='', max_length=4, null=True),
        ),
    ]
