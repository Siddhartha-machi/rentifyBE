# Generated by Django 4.2.4 on 2024-05-20 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentifyV1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentifyV1.location'),
        ),
    ]