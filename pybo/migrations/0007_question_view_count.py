# Generated by Django 3.1.3 on 2022-06-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0006_questioncount'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='view_count',
            field=models.TextField(default='0'),
        ),
    ]
