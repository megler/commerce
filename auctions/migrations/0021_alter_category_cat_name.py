# Generated by Django 4.0.2 on 2022-03-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_category_cat_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_name',
            field=models.CharField(choices=[('Brooms', 'Brooms'), ('Wands', 'Wands'), ('Capes', 'Capes')], default='Brooms', max_length=50),
        ),
    ]
