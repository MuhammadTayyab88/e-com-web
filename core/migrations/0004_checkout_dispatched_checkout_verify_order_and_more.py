# Generated by Django 5.1.2 on 2024-11-06 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_product_category_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='dispatched',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='verify_order',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]