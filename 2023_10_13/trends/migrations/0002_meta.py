# Generated by Django 4.2.6 on 2023-10-13 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trends', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('keyword_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trends.keyword')),
            ],
            bases=('trends.keyword',),
        ),
    ]