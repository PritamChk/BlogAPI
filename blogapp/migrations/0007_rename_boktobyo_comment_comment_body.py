# Generated by Django 4.0.2 on 2022-02-21 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_alter_blog_options_alter_blog_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='boktobyo',
            new_name='comment_body',
        ),
    ]