# Generated by Django 4.1.2 on 2022-11-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='tags',
            field=models.ManyToManyField(null=True, to='main.tag'),
        ),
    ]