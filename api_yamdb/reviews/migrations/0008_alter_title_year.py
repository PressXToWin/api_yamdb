# Generated by Django 3.2 on 2023-04-02 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_review_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(db_index=True, help_text='Укажите год публикации', verbose_name='Год публикации'),
        ),
    ]
