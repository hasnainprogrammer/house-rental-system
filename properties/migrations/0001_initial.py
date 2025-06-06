# Generated by Django 5.0.7 on 2024-07-31 18:58

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_title', models.CharField(max_length=200)),
                ('bathrooms', models.IntegerField()),
                ('bedrooms', models.IntegerField()),
                ('rooms', models.IntegerField()),
                ('price', models.IntegerField()),
                ('garage', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=20)),
                ('sqft', models.DecimalField(decimal_places=1, max_digits=5)),
                ('is_featured', models.BooleanField(default=False)),
                ('main_image', models.ImageField(upload_to='photos/')),
                ('image_1', models.ImageField(upload_to='photos/')),
                ('image_2', models.ImageField(upload_to='photos/')),
                ('image_3', models.ImageField(upload_to='photos/')),
                ('image_4', models.ImageField(upload_to='photos/')),
                ('list_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('wifi', models.BooleanField(default=False)),
                ('kitchen', models.BooleanField(default=False)),
                ('parking', models.BooleanField(default=False)),
                ('swimming_pool', models.BooleanField(default=False)),
                ('air_conditioning', models.BooleanField(default=False)),
                ('balcony', models.BooleanField(default=False)),
                ('tv', models.BooleanField(default=False)),
                ('laundry', models.BooleanField(default=False)),
                ('elevator_access', models.BooleanField(default=False)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('enquiry_date', models.DateTimeField(default=datetime.datetime.now)),
                ('owner_remarks', models.TextField()),
                ('remarks_date', models.DateTimeField(null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
        ),
    ]
