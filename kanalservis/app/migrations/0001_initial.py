# Generated by Django 4.0.4 on 2022-05-20 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_id', models.PositiveIntegerField(unique=True, verbose_name='№')),
                ('ord_num', models.PositiveIntegerField(unique=True, verbose_name='Заказ №')),
                ('ord_cost', models.PositiveIntegerField(verbose_name='Стоимость,$')),
                ('ord_date', models.DateField(verbose_name='Срок поставки')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
