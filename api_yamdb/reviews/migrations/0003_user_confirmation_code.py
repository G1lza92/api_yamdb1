# Generated by Django 2.2.16 on 2022-09-23 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_category_comment_genre_review_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=255, verbose_name='Код подтверждения'),
        ),
    ]