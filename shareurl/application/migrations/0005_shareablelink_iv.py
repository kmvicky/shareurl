# Generated by Django 2.2.7 on 2019-11-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_shareablelink_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareablelink',
            name='iv',
            field=models.TextField(blank=True, null=True),
        ),
    ]
