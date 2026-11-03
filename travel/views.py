"""
Django MVT Views & JSON AJAX Endpoints for Tourly.
Demonstrates:
- Session-based authentication & protected decorators
- Database CRUD operations with Django ORM
- Dynamic search, filtering, and sorting
- Asynchronous JSON responses for jQuery AJAX & AngularJS
"""
import json
from datetime import date
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST, require_GET

from .models import User, Destination, TourPackage, Booking, ContactMessage
from .forms import (
    RegistrationForm, LoginForm, BookingForm, ContactForm,
    DestinationAdminForm, TourPackageAdminForm
)


# --- Session Authentication Decorators ---

def tourly_login_required(view_func):
    """Ensure customer is logged in via Django session before accessing protected views."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('tourly_user_id'):
            messages.warning(request, "Please log in to access your travel dashboard or book a package.")
            return redirect(f"/login/?next={request.path}")
        return view_func(request, *args, **kwargs)
    return _wrapped


def tourly_admin_required(view_func):
    """Ensure user has administrator session privileges."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('tourly_user_id') or not request.session.get('tourly_is_admin'):
            messages.error(request, "Administrator privileges are required to view the Admin Dashboard.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped


# --- Customer Website Views ---

def home_view(request):
    """Render Homepage with popular destinations, featured tour packages, offers, and testimonials."""
    popular_names = ['Manali', 'Goa', 'Jaipur', 'Kashmir', 'Kerala', 'Shimla', 'Dubai', 'Bali']
    popular_destinations = Destination.objects.filter(name__in=popular_names)[:8]
    if popular_destinations.count() < 8:
        popular_destinations = Destination.objects.all()[:8]

    featured_packages = TourPackage.objects.select_related('destination').all()[:6]
    all_destinations = Destination.objects.all()

    # Serialize destinations for AngularJS interactive explorer component
    angular_destinations = [
        {
            'id': d.id,
            'name': d.name,
            'country': d.country,
            'category': d.category,
            'description': d.description,
            'image': d.image,
            'attractions': d.attractions_list(),
        }
        for d in all_destinations
    ]

    context = {
        'popular_destinations': popular_destinations,
        'featured_packages': featured_packages,
        'angular_destinations_json': json.dumps(angular_destinations),
        'categories': [c[0] for c in Destination.CATEGORY_CHOICES],
    }
    return render(request, 'home.html', context)


def destinations_view(request):
    """Destination listing page with search by name and filter by category."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    destinations = Destination.objects.all()
    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query) |
            Q(description__icontains=query) |
            Q(attractions__icontains=query)
        )
    if category:
        destinations = destinations.filter(category__iexact=category)

    angular_data = [
        {
            'id': d.id,
            'name': d.name,
            'country': d.country,
            'category': d.category,
            'description': d.description,
            'image': d.image,
            'attractions': d.attractions_list(),
        }
        for d in destinations
    ]

    context = {
        'destinations': destinations,
        'search_query': query,
        'selected_category': category,
        'categories': [c[0] for c in Destination.CATEGORY_CHOICES],
        'angular_destinations_json': json.dumps(angular_data),
    }
    return render(request, 'destinations.html', context)


def destination_detail_view(request, dest_id):
    """Individual destination detail page showing photographs, attractions, and packages."""
    destination = get_object_or_404(Destination, pk=dest_id)
    packages = TourPackage.objects.filter(destination=destination)
    related_destinations = Destination.objects.filter(
        category=destination.category
    ).exclude(pk=destination.id)[:3]

    context = {
        'destination': destination,
        'packages': packages,
        'related_destinations': related_destinations,
    }
    return render(request, 'destination_detail.html', context)


def packages_view(request):
    """Tour packages page with search, destination filter, budget filter, and price sorting."""
    query = request.GET.get('q', '').strip()
    dest_id = request.GET.get('destination', '').strip()
    category = request.GET.get('category', '').strip()
    max_budget = request.GET.get('max_budget', '').strip()
    sort_by = request.GET.get('sort', 'price_asc').strip()

    packages = TourPackage.objects.select_related('destination').all()

    if query:
        packages = packages.filter(
            Q(package_name__icontains=query) |
            Q(description__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(activities__icontains=query)
        )
    if dest_id.isdigit():
        packages = packages.filter(destination_id=int(dest_id))
    if category:
        packages = packages.filter(destination__category__iexact=category)
    if max_budget:
        try:
            packages = packages.filter(price__lte=float(max_budget))
        except ValueError:
            pass

    if sort_by == 'price_desc':
        packages = packages.order_by('-price')
    elif sort_by == 'name_asc':
        packages = packages.order_by('package_name')
    else:
        packages = packages.order_by('price')

    context = {
        'packages': packages,
        'destinations': Destination.objects.all(),
        'categories': [c[0] for c in Destination.CATEGORY_CHOICES],
        'search_query': query,
        'selected_destination': dest_id,
        'selected_category': category,
        'max_budget': max_budget,
        'sort_by': sort_by,
    }
    return render(request, 'packages.html', context)


def package_detail_view(request, pkg_id):
    """Detailed view of a single tour package including hotel info, activities, and day-wise itinerary."""
    package = get_object_or_404(TourPackage.objects.select_related('destination'), pk=pkg_id)
    similar_packages = TourPackage.objects.filter(
        destination__category=package.destination.category
    ).exclude(pk=package.id)[:3]

    context = {
        'package': package,
        'similar_packages': similar_packages,
    }
    return render(request, 'package_details.html', context)


def register_view(request):
    """Customer registration with backend validation and PBKDF2 password hashing."""
    if request.session.get('tourly_user_id'):
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            request.session['tourly_user_id'] = user.id
            request.session['tourly_user_name'] = user.name
            request.session['tourly_is_admin'] = user.is_admin
            messages.success(request, f"Welcome to Tourly, {user.name}! Your account has been created.")
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Customer & Admin login using Django session authentication."""
    if request.session.get('tourly_user_id'):
        return redirect('dashboard')

    next_url = request.GET.get('next', '/dashboard/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.verify_password(password):
                    request.session['tourly_user_id'] = user.id
                    request.session['tourly_user_name'] = user.name
                    request.session['tourly_is_admin'] = user.is_admin
                    messages.success(request, f"Welcome back, {user.name}!")
                    if user.is_admin:
                        return redirect('admin_dashboard')
                    return redirect(request.POST.get('next') or 'dashboard')
                else:
                    form.add_error(None, "Invalid email or password. Please try again.")
            except User.DoesNotExist:
                form.add_error(None, "No account found with that email address.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'next_url': next_url})


def logout_view(request):
    """Clear Django session and log out user."""
    request.session.flush()
    messages.info(request, "You have been logged out securely.")
    return redirect('home')


@tourly_login_required
def booking_view(request, pkg_id):
    """Booking creation form and submission handler."""
    package = get_object_or_404(TourPackage.objects.select_related('destination'), pk=pkg_id)
    user = get_object_or_404(User, pk=request.session['tourly_user_id'])

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = user
            booking.package = package
            booking.total_price = float(package.price) * int(booking.travelers)
            booking.booking_status = 'Pending'
            booking.save()
            messages.success(
                request,
                f"Booking Request #{booking.id} submitted for {package.package_name}! "
                f"Total Estimated Cost: ₹{booking.total_price:,.2f}."
            )
            return redirect('dashboard')
    else:
        form = BookingForm(initial={
            'customer_name': user.name,
            'customer_email': user.email,
            'customer_phone': user.phone,
            'travelers': 2,
        })

    context = {
        'package': package,
        'form': form,
        'today_iso': date.today().isoformat(),
    }
    return render(request, 'booking.html', context)


@tourly_login_required
def dashboard_view(request):
    """Protected Customer Dashboard showing personal info, upcoming trips, booking history, and status."""
    user = get_object_or_404(User, pk=request.session['tourly_user_id'])
    bookings = Booking.objects.select_related('package', 'package__destination').filter(user=user)

    today = date.today()
    upcoming_trips = bookings.filter(travel_date__gte=today).exclude(booking_status='Cancelled')
    past_or_cancelled = bookings.filter(Q(travel_date__lt=today) | Q(booking_status='Cancelled'))

    context = {
        'customer': user,
        'bookings': bookings,
        'upcoming_trips': upcoming_trips,
        'booking_history': past_or_cancelled,
        'total_bookings_count': bookings.count(),
        'confirmed_count': bookings.filter(booking_status='Confirmed').count(),
        'pending_count': bookings.filter(booking_status='Pending').count(),
    }
    return render(request, 'dashboard.html', context)


@tourly_login_required
@require_POST
def cancel_booking_view(request, booking_id):
    """Allow logged-in customer to cancel their own booking."""
    user_id = request.session['tourly_user_id']
    booking = get_object_or_404(Booking, pk=booking_id, user_id=user_id)
    if booking.booking_status in ['Pending', 'Confirmed']:
        booking.booking_status = 'Cancelled'
        booking.save()
        messages.warning(request, f"Booking #{booking.id} ({booking.package.package_name}) has been cancelled.")
    else:
        messages.info(request, f"Booking #{booking.id} cannot be cancelled (current status: {booking.booking_status}).")
    return redirect('dashboard')


def contact_view(request):
    """Contact Us page with JavaScript validation, Django POST handling, and AJAX support."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            messages.success(
                request,
                f"Thank you, {msg.name}! Your inquiry '{msg.subject}' has been recorded in our database."
            )
            return redirect('contact')
    else:
        initial = {}
        if request.session.get('tourly_user_id'):
            try:
                u = User.objects.get(pk=request.session['tourly_user_id'])
                initial = {'name': u.name, 'email': u.email, 'phone': u.phone}
            except User.DoesNotExist:
                pass
        form = ContactForm(initial=initial)

    return render(request, 'contact.html', {'form': form})


# --- Administrator Dashboard & CRUD Views ---

@tourly_admin_required
def admin_dashboard_view(request):
    """Administrator Dashboard with overview metrics and full management of Destinations, Packages, Bookings, Users, and Messages."""
    destinations = Destination.objects.all()
    packages = TourPackage.objects.select_related('destination').all()
    bookings = Booking.objects.select_related('user', 'package', 'package__destination').all()
    users = User.objects.all()
    contact_messages = ContactMessage.objects.all()

    context = {
        'total_users': users.count(),
        'total_destinations': destinations.count(),
        'total_packages': packages.count(),
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(booking_status='Pending').count(),
        'confirmed_bookings': bookings.filter(booking_status='Confirmed').count(),
        'cancelled_bookings': bookings.filter(booking_status='Cancelled').count(),
        'completed_bookings': bookings.filter(booking_status='Completed').count(),
        'destinations': destinations,
        'packages': packages,
        'bookings': bookings,
        'users': users,
        'contact_messages': contact_messages,
        'categories': [c[0] for c in Destination.CATEGORY_CHOICES],
    }
    return render(request, 'admin_dashboard.html', context)


@tourly_admin_required
@require_POST
def admin_save_destination(request):
    """Create or Update a Destination from the Admin Dashboard."""
    dest_id = request.POST.get('destination_id')
    if dest_id:
        instance = get_object_or_404(Destination, pk=dest_id)
        form = DestinationAdminForm(request.POST, instance=instance)
        action_word = "updated"
    else:
        form = DestinationAdminForm(request.POST)
        action_word = "added"

    if form.is_valid():
        dest = form.save()
        messages.success(request, f"Destination '{dest.name}' successfully {action_word}.")
    else:
        messages.error(request, f"Error saving destination: {form.errors.as_text()}")
    return redirect('admin_dashboard')


@tourly_admin_required
@require_POST
def admin_delete_destination(request, dest_id):
    """Delete a Destination from the Admin Dashboard."""
    dest = get_object_or_404(Destination, pk=dest_id)
    name = dest.name
    dest.delete()
    messages.warning(request, f"Destination '{name}' has been deleted.")
    return redirect('admin_dashboard')


@tourly_admin_required
@require_POST
def admin_save_package(request):
    """Create or Update a Tour Package from the Admin Dashboard."""
    pkg_id = request.POST.get('package_id')
    if pkg_id:
        instance = get_object_or_404(TourPackage, pk=pkg_id)
        form = TourPackageAdminForm(request.POST, instance=instance)
        action_word = "updated"
    else:
        form = TourPackageAdminForm(request.POST)
        action_word = "added"

    if form.is_valid():
        pkg = form.save()
        messages.success(request, f"Tour Package '{pkg.package_name}' successfully {action_word}.")
    else:
        messages.error(request, f"Error saving tour package: {form.errors.as_text()}")
    return redirect('admin_dashboard')


@tourly_admin_required
@require_POST
def admin_delete_package(request, pkg_id):
    """Delete a Tour Package from the Admin Dashboard."""
    pkg = get_object_or_404(TourPackage, pk=pkg_id)
    name = pkg.package_name
    pkg.delete()
    messages.warning(request, f"Tour Package '{name}' has been deleted.")
    return redirect('admin_dashboard')


@tourly_admin_required
@require_POST
def admin_update_booking_status(request, booking_id):
    """Standard form POST endpoint to update booking status."""
    booking = get_object_or_404(Booking, pk=booking_id)
    new_status = request.POST.get('booking_status')
    valid_statuses = [s[0] for s in Booking.STATUS_CHOICES]
    if new_status in valid_statuses:
        booking.booking_status = new_status
        booking.save()
        messages.success(request, f"Booking #{booking.id} status updated to {new_status}.")
    return redirect('admin_dashboard')


# --- jQuery AJAX JSON Endpoints ---

@require_GET
def api_search_destinations(request):
    """AJAX endpoint: Search and filter destinations without reloading the page."""
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    qs = Destination.objects.all()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(country__icontains=q) |
            Q(description__icontains=q) |
            Q(attractions__icontains=q)
        )
    if category:
        qs = qs.filter(category__iexact=category)

    results = [
        {
            'id': d.id,
            'name': d.name,
            'country': d.country,
            'category': d.category,
            'description': d.description,
            'image': d.image,
            'attractions': d.attractions_list(),
            'detail_url': f"/destinations/{d.id}/",
        }
        for d in qs
    ]
    return JsonResponse({'status': 'ok', 'count': len(results), 'destinations': results})


@require_GET
def api_filter_packages(request):
    """AJAX endpoint: Dynamically filter and sort tour packages."""
    q = request.GET.get('q', '').strip()
    destination_id = request.GET.get('destination', '').strip()
    category = request.GET.get('category', '').strip()
    max_budget = request.GET.get('max_budget', '').strip()
    sort_by = request.GET.get('sort', 'price_asc').strip()

    qs = TourPackage.objects.select_related('destination').all()
    if q:
        qs = qs.filter(
            Q(package_name__icontains=q) |
            Q(description__icontains=q) |
            Q(destination__name__icontains=q)
        )
    if destination_id.isdigit():
        qs = qs.filter(destination_id=int(destination_id))
    if category:
        qs = qs.filter(destination__category__iexact=category)
    if max_budget:
        try:
            qs = qs.filter(price__lte=float(max_budget))
        except ValueError:
            pass

    if sort_by == 'price_desc':
        qs = qs.order_by('-price')
    elif sort_by == 'name_asc':
        qs = qs.order_by('package_name')
    else:
        qs = qs.order_by('price')

    packages_data = [
        {
            'id': p.id,
            'package_name': p.package_name,
            'destination_id': p.destination.id,
            'destination_name': p.destination.name,
            'category': p.destination.category,
            'duration': p.duration,
            'price': float(p.price),
            'image': p.image,
            'description': p.description,
            'hotel_info': p.hotel_info,
            'availability': p.availability,
            'activities': p.activities_list(),
            'itinerary': p.itinerary_days(),
            'detail_url': f"/packages/{p.id}/",
            'book_url': f"/booking/{p.id}/",
        }
        for p in qs
    ]
    return JsonResponse({'status': 'ok', 'count': len(packages_data), 'packages': packages_data})


@require_GET
def api_package_detail(request, pkg_id):
    """AJAX endpoint: Load single tour package details asynchronously for modal preview."""
    p = get_object_or_404(TourPackage.objects.select_related('destination'), pk=pkg_id)
    return JsonResponse({
        'status': 'ok',
        'package': {
            'id': p.id,
            'package_name': p.package_name,
            'destination_name': p.destination.name,
            'country': p.destination.country,
            'category': p.destination.category,
            'duration': p.duration,
            'price': float(p.price),
            'image': p.image,
            'description': p.description,
            'hotel_info': p.hotel_info,
            'availability': p.availability,
            'activities': p.activities_list(),
            'itinerary': p.itinerary_days(),
            'book_url': f"/booking/{p.id}/",
        }
    })


@require_POST
def api_submit_contact(request):
    """AJAX endpoint: Submit Contact Us form asynchronously with CSRF protection."""
    form = ContactForm(request.POST)
    if form.is_valid():
        msg = form.save()
        return JsonResponse({
            'status': 'ok',
            'message': f"Thank you, {msg.name}! Your message (#{msg.id}) has been saved to MySQL.",
            'message_id': msg.id,
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@tourly_login_required
@require_GET
def api_booking_info(request, booking_id):
    """AJAX endpoint: Retrieve detailed booking record asynchronously."""
    user_id = request.session['tourly_user_id']
    is_admin = request.session.get('tourly_is_admin', False)
    if is_admin:
        b = get_object_or_404(Booking.objects.select_related('package', 'package__destination', 'user'), pk=booking_id)
    else:
        b = get_object_or_404(Booking.objects.select_related('package', 'package__destination', 'user'), pk=booking_id, user_id=user_id)

    return JsonResponse({
        'status': 'ok',
        'booking': {
            'id': b.id,
            'customer_name': b.customer_name,
            'customer_email': b.customer_email,
            'customer_phone': b.customer_phone,
            'package_name': b.package.package_name,
            'destination_name': b.package.destination.name,
            'duration': b.package.duration,
            'hotel_info': b.package.hotel_info,
            'travel_date': b.travel_date.isoformat(),
            'travelers': b.travelers,
            'total_price': float(b.total_price),
            'special_requirements': b.special_requirements or 'None specified',
            'booking_status': b.booking_status,
            'created_at': b.created_at.strftime('%d %b %Y, %I:%M %p'),
        }
    })


@tourly_admin_required
@require_POST
def api_admin_update_booking(request):
    """AJAX endpoint: Update booking status dynamically from the Admin Dashboard."""
    booking_id = request.POST.get('booking_id')
    new_status = request.POST.get('booking_status')
    valid_statuses = [s[0] for s in Booking.STATUS_CHOICES]

    if not booking_id or new_status not in valid_statuses:
        return JsonResponse({'status': 'error', 'message': 'Invalid booking ID or status.'}, status=400)

    booking = get_object_or_404(Booking, pk=booking_id)
    booking.booking_status = new_status
    booking.save()

    return JsonResponse({
        'status': 'ok',
        'booking_id': booking.id,
        'new_status': booking.booking_status,
        'message': f"Booking #{booking.id} status updated to {booking.booking_status}."
    })
