# Generated by Django 4.1 on 2024-01-12 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_alter_group_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TvIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'ТВ идентификатор',
                'verbose_name_plural': 'ТВ идентификаторы',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='tv_identifiers',
            field=models.ManyToManyField(blank=True, to='groups.tvidentifier'),
        ),
    ]
