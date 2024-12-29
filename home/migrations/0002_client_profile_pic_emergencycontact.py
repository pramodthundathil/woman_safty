# Generated by Django 5.0.6 on 2024-12-29 06:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='propic'),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.PositiveIntegerField()),
                ('relationship', models.CharField(blank=True, choices=[('parent', 'Parent'), ('sibling', 'Sibling'), ('friend', 'Friend'), ('spouse', 'Spouse'), ('other', 'Other')], max_length=255, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
