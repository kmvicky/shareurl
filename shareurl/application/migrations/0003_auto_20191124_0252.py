# Generated by Django 2.2.7 on 2019-11-24 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20191124_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shareablelink',
            name='is_shared',
        ),
        migrations.RemoveField(
            model_name='shareablelink',
            name='text',
        ),
        migrations.AddField(
            model_name='shareablelink',
            name='title',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]