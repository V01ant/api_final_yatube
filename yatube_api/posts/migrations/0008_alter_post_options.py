# Generated by Django 3.2.16 on 2023-02-12 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_rename_author_follow_following'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['pub_date']},
        ),
    ]
