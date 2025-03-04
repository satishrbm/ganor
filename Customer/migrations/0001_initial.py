# Generated by Django 4.2.6 on 2023-10-14 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0001_initial'),
        ('Route', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order_number', models.IntegerField()),
                ('Sequence', models.IntegerField(null=True)),
                ('Stand', models.BooleanField(default=False)),
                ('Customer_name', models.CharField(max_length=100)),
                ('Nick_name', models.CharField(blank=True, max_length=200)),
                ('C_name', models.CharField(max_length=100)),
                ('N_name', models.CharField(max_length=100)),
                ('work', models.CharField(blank=True, max_length=200)),
                ('House_number', models.CharField(blank=True, max_length=200)),
                ('Society', models.CharField(blank=True, max_length=200)),
                ('Area', models.CharField(blank=True, max_length=200)),
                ('Pincode', models.CharField(blank=True, max_length=10)),
                ('Mobile_number1', models.CharField(max_length=20)),
                ('Mobile_number2', models.CharField(max_length=20, null=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Started_at', models.DateField()),
                ('End_date', models.DateField()),
                ('Current_status', models.CharField(max_length=20)),
                ('Morning_bottle', models.FloatField(blank=True, null=True)),
                ('Milk_delivery_frequency', models.CharField(choices=[('1', 'Daily'), ('2', 'Every Other Day'), ('3', 'Weekly')], default='1', max_length=20)),
                ('Frequency1', models.FloatField(blank=True)),
                ('Frequency2', models.FloatField(blank=True)),
                ('Saturday', models.BooleanField(blank=True, default=False)),
                ('Sunday', models.BooleanField(blank=True, default=False)),
                ('Further_account', models.FloatField(blank=True, null=True)),
                ('Credit_debit', models.CharField(blank=True, max_length=20, null=True)),
                ('Customer_rate', models.FloatField(null=True)),
                ('Created_at', models.DateField(auto_now=True)),
                ('Updated_at', models.DateField(null=True)),
                ('Total_bottle', models.IntegerField(blank=True, null=True)),
                ('Return_bottle', models.IntegerField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('Cutomer_route', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Route.route')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Supply_date', models.DateField()),
                ('Today_cost', models.FloatField()),
                ('Today_bottle', models.IntegerField()),
                ('Today_return_bottle', models.IntegerField(blank=True)),
                ('Total_cost', models.FloatField()),
                ('Total_bottle', models.IntegerField(blank=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplies', to='Customer.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sequence_number', models.IntegerField(null=True)),
                ('updated_at', models.DateField(null=True)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customers')),
                ('Route', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Route.route')),
            ],
        ),
    ]
