# Generated by Django 5.0.3 on 2024-05-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='cnpj',
            field=models.CharField(max_length=18, verbose_name='CNPJ'),
        ),
    ]