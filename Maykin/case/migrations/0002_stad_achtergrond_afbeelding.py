# Generated by Django 5.0.3 on 2024-09-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stad',
            name='achtergrond_afbeelding',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
