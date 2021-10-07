# Generated by Django 3.2.5 on 2021-10-06 02:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('local', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localgames',
            name='players',
            field=models.ManyToManyField(related_name='local_games', to=settings.AUTH_USER_MODEL),
        ),
    ]
