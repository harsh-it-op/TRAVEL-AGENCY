# Generated initial migration for Tourly travel app
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Users',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('country', models.CharField(default='India', max_length=100)),
                ('category', models.CharField(choices=[('Adventure', 'Adventure'), ('Beaches', 'Beaches'), ('Mountains', 'Mountains'), ('Historical Places', 'Historical Places'), ('Honeymoon', 'Honeymoon'), ('Wildlife', 'Wildlife')], max_length=50)),
                ('description', models.TextField()),
                ('image', models.CharField(default='/static/images/manali.svg', max_length=255)),
                ('attractions', models.TextField(help_text='Comma-separated popular attractions')),
            ],
            options={
                'db_table': 'Destinations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ContactMessages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TourPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('duration', models.CharField(help_text='e.g. 5 Days / 4 Nights', max_length=60)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.CharField(default='/static/images/manali.svg', max_length=255)),
                ('hotel_info', models.CharField(default='4-Star Deluxe Resort with Breakfast & Dinner', max_length=255)),
                ('activities', models.TextField(default='Guided Sightseeing, Cultural Evening, Local Transfers, Adventure Excursion')),
                ('itinerary', models.TextField(help_text='Newline or pipe-separated day-wise itinerary')),
                ('availability', models.CharField(default='Available Daily (Nov 2026 - Jun 2027)', max_length=180)),
                ('destination', models.ForeignKey(db_column='destination_id', on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='travel.destination')),
            ],
            options={
                'db_table': 'TourPackages',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=120)),
                ('customer_email', models.EmailField(max_length=150)),
                ('customer_phone', models.CharField(max_length=20)),
                ('travel_date', models.DateField()),
                ('travelers', models.PositiveIntegerField(default=2)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('special_requirements', models.TextField(blank=True, default='')),
                ('booking_status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(db_column='package_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='travel.tourpackage')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='travel.user')),
            ],
            options={
                'db_table': 'Bookings',
                'ordering': ['-created_at'],
            },
        ),
    ]
