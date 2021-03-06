# Generated by Django 3.0.7 on 2020-09-02 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('frequency', models.PositiveIntegerField(verbose_name='frequency')),
                ('currency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scrapper', to='api.Currency', verbose_name='currency')),
            ],
            options={
                'verbose_name': 'Scraper',
                'verbose_name_plural': 'Scrapers',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('value', models.FloatField(verbose_name='value')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='api.Currency', verbose_name='currency')),
            ],
            options={
                'verbose_name': 'price',
                'verbose_name_plural': 'prices',
                'ordering': ('created_at',),
            },
        ),
    ]
