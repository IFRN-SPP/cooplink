# Generated by Django 5.0.3 on 2024-05-03 01:32

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, verbose_name='Número')),
                ('start', models.DateField(verbose_name='Data de Início')),
                ('end', models.DateField(verbose_name='Data de Término')),
                ('active', models.BooleanField(default=False, verbose_name='Situção')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome da Instituição')),
                ('cnpj', models.CharField(max_length=14, verbose_name='CNPJ')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Produto')),
                ('unit', models.CharField(choices=[('KG', 'KG'), ('UNI', 'UNI')], max_length=3, verbose_name='Unidade de Medida')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CallProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
                ('balance', models.IntegerField(default=None, verbose_name='Saldo')),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.call', verbose_name='Chamada')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='call', to='app.product', verbose_name='Produto')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='call',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.institution', verbose_name='Instituição'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.institution', verbose_name='Instituição')),
            ],
            options={
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('approved', 'Aprovado'), ('denied', 'Negado'), ('delivered', 'Entregue')], default='pending', max_length=10, verbose_name='Situação')),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.call', verbose_name='Chamada')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.institution', verbose_name='Instituição')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_quantity', models.IntegerField(default=None, verbose_name='Quant. Pedida')),
                ('available_quantity', models.IntegerField(blank=True, null=True, verbose_name='Quant. Disponível')),
                ('status', models.CharField(choices=[('parcial', 'Parcial'), ('available', 'Disponível'), ('denied', 'Negado')], default='available', max_length=10, verbose_name='Situção')),
                ('call_product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='app.callproduct', verbose_name='Produto da Chamada')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_products', to='app.order', verbose_name='Pedido')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
