# Generated by Django 3.2 on 2023-03-30 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=256, unique=True, verbose_name='Категория')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название жанра', max_length=256, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-year', 'name'), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, help_text='Введите описание произведения', null=True, verbose_name='Описание произведения'),
        ),
        migrations.AddField(
            model_name='title',
            name='name',
            field=models.CharField(default=' ', help_text='Введите название произведения', max_length=256, verbose_name='Произведение'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.review', verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(default=1, help_text='Укажите год публикации', verbose_name='Год публикации'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.genre', verbose_name='Жанр')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Произведение и жанр',
                'verbose_name_plural': 'Произведения и жанры',
            },
        ),
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Выберите категорию по желанию', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категорию произведения'),
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.GenreTitle', to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AddConstraint(
            model_name='genretitle',
            constraint=models.UniqueConstraint(fields=('genre', 'title'), name='unique_genre_title'),
        ),
    ]
