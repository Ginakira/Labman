# Generated by Django 3.0.7 on 2020-06-25 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labman', '0006_auto_20200625_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='publisher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]