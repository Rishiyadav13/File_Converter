# Generated by Django 5.0.6 on 2024-06-30 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_user_managers_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaptchaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('captcha_text', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]