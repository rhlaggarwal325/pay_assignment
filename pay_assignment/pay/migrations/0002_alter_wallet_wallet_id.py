# Generated by Django 3.2.7 on 2021-09-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
