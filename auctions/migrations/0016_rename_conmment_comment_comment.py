# Generated by Django 4.0.2 on 2022-03-06 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_rename_description_comment_conmment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='conmment',
            new_name='comment',
        ),
    ]
