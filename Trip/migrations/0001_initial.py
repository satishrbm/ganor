# Generated by Django 4.2.6 on 2023-10-14 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Customer', '0001_initial'),
        ('Delivery_boy', '0001_initial'),
        ('Route', '0001_initial'),
        ('Vehicles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Trip_number', models.CharField(max_length=100)),
                ('Trip_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('Customer_list', models.ManyToManyField(blank=True, null=True, to='Customer.customers')),
                ('Delivery_boy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Delivery_boy.delivery_boy')),
                ('Route_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Route.route')),
                ('Vehicle_number', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Vehicles.vehicle')),
            ],
        ),
    ]
