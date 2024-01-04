# Generated by Django 4.2.6 on 2024-01-02 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Creator', '0016_alter_music_album'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollabNotifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Msg', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Crid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Collab_notification_receiver', to='Creator.creators')),
                ('FlwCrid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Collab_notification_generator', to='Creator.creators')),
            ],
        ),
    ]
