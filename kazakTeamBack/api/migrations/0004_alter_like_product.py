# Generated by Django 3.2 on 2023-05-03 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_like_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.product'),
        ),
    ]
