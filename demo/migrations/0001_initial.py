# Generated by Django 2.1.7 on 2019-03-07 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedBMI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('underweight', models.TextField()),
                ('normal', models.TextField()),
                ('overweight', models.TextField()),
                ('obese', models.TextField()),
            ],
        ),
    ]