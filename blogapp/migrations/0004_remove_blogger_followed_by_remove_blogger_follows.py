# Generated by Django 4.0.2 on 2022-02-20 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_blogger_followed_by_blogger_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogger',
            name='followed_by',
        ),
        migrations.RemoveField(
            model_name='blogger',
            name='follows',
        ),
    ]
