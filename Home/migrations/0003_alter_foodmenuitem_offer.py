# Generated by Django 5.0.6 on 2024-10-28 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_foodmenuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenuitem',
            name='offer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
