# Generated by Django 3.2.5 on 2021-09-07 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render_doc', '0008_historicalblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalblock',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]