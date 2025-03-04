# Generated by Django 4.2.6 on 2023-10-14 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Vehicle_type', models.CharField(max_length=128)),
                ('Vehicle_number', models.CharField(max_length=128)),
                ('Vehicle_owner', models.CharField(max_length=128)),
                ('Vehicle_owner_type', models.CharField(max_length=128)),
                ('Vehicle_price', models.FloatField(max_length=128)),
                ('Vehicle_purchase_date', models.CharField(max_length=128)),
                ('Vehicle_average', models.CharField(max_length=128)),
                ('Vehicle_puc', models.CharField(max_length=128)),
                ('Vehicle_puc_date', models.CharField(max_length=128)),
                ('Vehicle_insurance', models.CharField(max_length=128)),
                ('Vehicle_insurance_date', models.CharField(max_length=128)),
                ('Vehicle_status', models.BooleanField()),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
