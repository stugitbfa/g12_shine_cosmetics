# Generated by Django 5.2.3 on 2025-06-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0005_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')], default='new', max_length=20),
        ),
    ]
