# Generated by Django 4.0.4 on 2022-05-26 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailuser',
            old_name='firstname',
            new_name='firstName',
        ),
    ]