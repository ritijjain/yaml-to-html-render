# Generated by Django 3.2.5 on 2021-07-29 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('render_doc', '0003_block_yaml_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='yaml_data',
        ),
    ]
