# Generated by Django 4.0.2 on 2022-03-06 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_name',
            field=models.CharField(default='Brooms', max_length=50, null=True),
        ),
    ]
