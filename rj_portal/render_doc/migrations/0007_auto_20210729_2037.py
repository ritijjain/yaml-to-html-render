# Generated by Django 3.2.5 on 2021-07-29 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render_doc', '0006_block_text_yaml'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='text_blob',
        ),
        migrations.RemoveField(
            model_name='block',
            name='text_yaml',
        ),
        migrations.AlterField(
            model_name='block',
            name='data',
            field=models.TextField(blank=True, null=True),
        ),
    ]