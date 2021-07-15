# Generated by Django 3.2.5 on 2021-07-15 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('symbol', models.CharField(max_length=10)),
                ('industry', models.CharField(default='', max_length=50, null=True)),
                ('market_cap', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('current_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('volume', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('prev_high', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('prev_low', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('price_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('percent_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(null=True)),
                ('yhat_30', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_30_upper', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_30_lower', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_30_advice', models.CharField(default='', max_length=20, null=True)),
                ('yhat_180', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_180_upper', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_180_lower', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_180_advice', models.CharField(default='', max_length=20, null=True)),
                ('yhat_365', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_365_upper', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_365_lower', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('yhat_365_advice', models.CharField(default='', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_stock', to='stocks.stock')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('trans_date', models.DateTimeField()),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_stock', to='stocks.stock')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Historical_Stock_Data',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_recorded', models.DateTimeField()),
                ('price_open', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price_close', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price_high', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price_low', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('volume', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_forecast_id', to='stocks.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Forecast_Record',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('yhat', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('yhat_upper', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('yhat_lower', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_data_id', to='stocks.stock')),
            ],
        ),
    ]
