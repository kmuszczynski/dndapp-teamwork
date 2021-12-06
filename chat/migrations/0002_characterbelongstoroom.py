# Generated by Django 3.2.8 on 2021-12-06 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charsheets', '0001_initial'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterBelongsToRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charsheets.character')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatroom')),
            ],
        ),
    ]
