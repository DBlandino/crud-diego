# Generated by Django 3.2.9 on 2021-12-01 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_usuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sobre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=99999)),
            ],
        ),
    ]
