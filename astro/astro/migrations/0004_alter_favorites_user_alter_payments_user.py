# Generated by Django 4.0.4 on 2022-10-28 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0003_rename_note_histpersons_types_alter_favorites_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
