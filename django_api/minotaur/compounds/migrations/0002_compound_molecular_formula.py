# Generated by Django 3.1.2 on 2020-10-12 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compound',
            name='molecular_formula',
            field=models.CharField(default='null', max_length=50),
            preserve_default=False,
        ),
    ]
