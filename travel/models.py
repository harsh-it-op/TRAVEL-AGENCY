"""
Django ORM Models for Tourly – Travel Agency Management and Booking System.
Maps directly to the MySQL relational schema:
- Users
- Destinations
- TourPackages
- Bookings
- ContactMessages
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    """Customer and Administrator user table (`Users` in MySQL)."""
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Users'
        ordering = ['-created_at']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Destination(models.Model):
    """Travel destination table (`Destinations` in MySQL)."""
    CATEGORY_CHOICES = [
        ('Adventure', 'Adventure'),
        ('Beaches', 'Beaches'),
        ('Mountains', 'Mountains'),
        ('Historical Places', 'Historical Places'),
        ('Honeymoon', 'Honeymoon'),
        ('Wildlife', 'Wildlife'),
    ]

    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=100, default='India')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.CharField(max_length=255, default='/static/images/manali.svg')
    attractions = models.TextField(help_text='Comma-separated popular attractions')

    class Meta:
        db_table = 'Destinations'
        ordering = ['name']

    def attractions_list(self):
        return [a.strip() for a in self.attractions.split(',') if a.strip()]

    def __str__(self):
        return f"{self.name}, {self.country} ({self.category})"


class TourPackage(models.Model):
    """Tour package table (`TourPackages` in MySQL) linked to Destination via Foreign Key."""
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='packages',
        db_column='destination_id'
    )
    package_name = models.CharField(max_length=180)
    description = models.TextField()
    duration = models.CharField(max_length=60, help_text='e.g. 5 Days / 4 Nights')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, default='/static/images/manali.svg')
    hotel_info = models.CharField(
        max_length=255,
        default='4-Star Deluxe Resort with Breakfast & Dinner'
    )
    activities = models.TextField(
        default='Guided Sightseeing, Cultural Evening, Local Transfers, Adventure Excursion'
    )
    itinerary = models.TextField(help_text='Newline or pipe-separated day-wise itinerary')
    availability = models.CharField(
        max_length=180,
        default='Available Daily (Nov 2026 - Jun 2027)'
    )

    class Meta:
        db_table = 'TourPackages'
        ordering = ['price']

    def activities_list(self):
        return [act.strip() for act in self.activities.split(',') if act.strip()]

    def itinerary_days(self):
        return [day.strip() for day in self.itinerary.split('|') if day.strip()]

    def __str__(self):
        return f"{self.package_name} - ₹{self.price}"


class Booking(models.Model):
    """Customer travel booking table (`Bookings` in MySQL)."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_column='user_id'
    )
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_column='package_id'
    )
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField(max_length=150)
    customer_phone = models.CharField(max_length=20)
    travel_date = models.DateField()
    travelers = models.PositiveIntegerField(default=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    special_requirements = models.TextField(blank=True, default='')
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Bookings'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.package_id and self.travelers:
            self.total_price = float(self.package.price) * int(self.travelers)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer_name} ({self.booking_status})"


class ContactMessage(models.Model):
    """Customer inquiry messages (`ContactMessages` in MySQL)."""
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ContactMessages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} from {self.name}"
