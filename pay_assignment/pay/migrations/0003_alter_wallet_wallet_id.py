# Generated by Django 3.2.7 on 2021-09-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_alter_wallet_wallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
