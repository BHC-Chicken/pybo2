# Generated by Django 3.1.3 on 2022-06-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0010_auto_20220619_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='view_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
