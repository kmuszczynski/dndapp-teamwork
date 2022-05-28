# Generated by Django 3.2.8 on 2022-05-28 16:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('columns', models.PositiveBigIntegerField()),
                ('rows', models.PositiveBigIntegerField()),
                ('status', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatroom')),
            ],
        ),
        migrations.CreateModel(
            name='GridAreaWithCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.PositiveBigIntegerField()),
                ('row', models.PositiveBigIntegerField()),
                ('character', models.CharField(max_length=50)),
                ('grid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grid.grid')),
            ],
        ),
    ]
