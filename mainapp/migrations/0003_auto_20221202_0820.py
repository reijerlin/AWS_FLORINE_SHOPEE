# Generated by Django 3.2.15 on 2022-12-02 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_allorders_getyyyymm_getyyyymmdd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allorders',
            name='COMMODITY_NM',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='allorders',
            name='SHIIPPING_CODE',
            field=models.CharField(max_length=30),
        ),
    ]
