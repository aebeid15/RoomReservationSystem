# Generated by Django 5.1.3 on 2024-11-20 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='equipment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.Field(max_length=128),
        ),
    ]