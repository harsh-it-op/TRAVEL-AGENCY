"""
Automated Unit & Integration Test Suite for Tourly.
Run with:
    TOURLY_USE_SQLITE=True python3 manage.py test
    or (when MySQL is running):
    python3 manage.py test
"""
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Destination, TourPackage, Booking, ContactMessage


class TourlyFullStackTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Admin and Customer users
        self.admin = User(name="Admin User", email="admin@tourly.com", phone="+91-9876543210", is_admin=True)
        self.admin.set_password("Admin@123")
        self.admin.save()

        self.customer = User(name="Priya Verma", email="priya@example.com", phone="+91-9811122334", is_admin=False)
        self.customer.set_password("Travel@123")
        self.customer.save()

        # Create Destination & Package
        self.dest = Destination.objects.create(
            name="Manali",
            country="India",
            category="Mountains",
            description="Alpine valley in Himachal Pradesh.",
            image="/static/images/manali.svg",
            attractions="Solang Valley, Rohtang Pass",
        )
        self.pkg = TourPackage.objects.create(
            destination=self.dest,
            package_name="Himalayan Snow Adventure",
            description="5-day guided snow tour.",
            duration="5 Days / 4 Nights",
            price=18500.00,
            hotel_info="4-Star Resort",
            activities="Paragliding, Rafting",
            itinerary="Day 1: Arrival | Day 2: Solang",
            availability="Available Daily",
        )

    def test_homepage_and_destinations_load(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Discover Your Next Adventure")

        dest_res = self.client.get(reverse('destinations'))
        self.assertEqual(dest_res.status_code, 200)
        self.assertContains(dest_res, "Manali")

    def test_user_registration_and_login(self):
        reg_res = self.client.post(reverse('register'), {
            'full_name': 'Karan Johar',
            'email': 'karan@example.com',
            'phone': '+91-9988776655',
            'password': 'SecurePassword123',
            'confirm_password': 'SecurePassword123',
        })
        self.assertEqual(reg_res.status_code, 302)
        self.assertTrue(User.objects.filter(email='karan@example.com').exists())

    def test_booking_workflow_and_admin_ajax_status_update(self):
        # Log in as customer
        session = self.client.session
        session['tourly_user_id'] = self.customer.id
        session['tourly_is_admin'] = False
        session.save()

        travel_dt = (date.today() + timedelta(days=15)).isoformat()
        book_res = self.client.post(reverse('booking', args=[self.pkg.id]), {
            'customer_name': 'Priya Verma',
            'customer_email': 'priya@example.com',
            'customer_phone': '+91-9811122334',
            'travel_date': travel_dt,
            'travelers': 3,
            'special_requirements': 'Window seat transfer',
        })
        self.assertEqual(book_res.status_code, 302)
        booking = Booking.objects.first()
        self.assertIsNotNone(booking)
        self.assertEqual(float(booking.total_price), 18500.00 * 3)
        self.assertEqual(booking.booking_status, 'Pending')

        # Admin AJAX update
        session = self.client.session
        session['tourly_user_id'] = self.admin.id
        session['tourly_is_admin'] = True
        session.save()

        ajax_res = self.client.post(reverse('api_admin_update_booking'), {
            'booking_id': booking.id,
            'booking_status': 'Confirmed',
        })
        self.assertEqual(ajax_res.status_code, 200)
        booking.refresh_from_db()
        self.assertEqual(booking.booking_status, 'Confirmed')

    def test_ajax_json_endpoints(self):
        search_res = self.client.get(reverse('api_search_destinations'), {'q': 'Manali'})
        self.assertEqual(search_res.status_code, 200)
        self.assertEqual(search_res.json()['count'], 1)

        contact_res = self.client.post(reverse('api_submit_contact'), {
            'name': 'Rahul Dravid',
            'email': 'rahul@example.com',
            'phone': '+91-9812345678',
            'subject': 'Family Tour Inquiry',
            'message': 'Looking for a 5-day Manali itinerary in December.',
        })
        self.assertEqual(contact_res.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
