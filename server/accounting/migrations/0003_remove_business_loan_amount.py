# Generated by Django 4.2.6 on 2023-10-22 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_remove_business_provider_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='loan_amount',
        ),
    ]
