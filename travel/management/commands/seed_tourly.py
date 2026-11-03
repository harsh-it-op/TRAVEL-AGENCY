"""
Django management command `python manage.py seed_tourly`
Populates the database with:
- 2 Default Users (1 Admin, 1 Customer)
- 10 Destinations across all 6 syllabus categories
- 16 Comprehensive Tour Packages with itineraries, hotels, and activities
- Sample Bookings and Contact Messages
"""
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from travel.models import User, Destination, TourPackage, Booking, ContactMessage


DESTINATIONS_DATA = [
    {
        'name': 'Manali',
        'country': 'India',
        'category': 'Mountains',
        'image': '/static/images/manali.svg',
        'description': 'Nestled in the Pir Panjal and Dhauladhar ranges of Himachal Pradesh, Manali offers snow-clad peaks, cedar forests, river rafting on the Beas, and high-altitude passes.',
        'attractions': 'Solang Valley, Rohtang Pass, Hadimba Devi Temple, Old Manali Cafe Trail, Atal Tunnel, Jogini Waterfall',
    },
    {
        'name': 'Goa',
        'country': 'India',
        'category': 'Beaches',
        'image': '/static/images/goa.svg',
        'description': 'India\'s premier coastal paradise blending golden Arabian Sea beaches, Portuguese heritage cathedrals, vibrant beach shacks, and thrilling water sports.',
        'attractions': 'Baga & Calangute Beach, Palolem Bay, Basilica of Bom Jesus, Dudhsagar Falls, Aguada Fort, Mandovi Sunset Cruise',
    },
    {
        'name': 'Jaipur',
        'country': 'India',
        'category': 'Historical Places',
        'image': '/static/images/jaipur.svg',
        'description': 'The Pink City of Rajasthan, famed for royal Rajputana forts, astronomical observatories, ornate palaces, and bustling traditional craft bazaars.',
        'attractions': 'Amber Fort, Hawa Mahal, City Palace, Jantar Mantar, Nahargarh Sunset Point, Johari Bazaar',
    },
    {
        'name': 'Kashmir',
        'country': 'India',
        'category': 'Honeymoon',
        'image': '/static/images/kashmir.svg',
        'description': 'Celebrated as Paradise on Earth, featuring serene shikara rides on Dal Lake, Mughal terraced gardens, alpine meadows in Gulmarg, and Lidder valley views.',
        'attractions': 'Dal Lake Houseboats, Gulmarg Gondola, Pahalgam Betaab Valley, Sonamarg Thajiwas Glacier, Shalimar Bagh',
    },
    {
        'name': 'Kerala',
        'country': 'India',
        'category': 'Wildlife',
        'image': '/static/images/kerala.svg',
        'description': 'God\'s Own Country enchants travelers with emerald backwaters in Alleppey, misty tea estates in Munnar, Ayurvedic retreats, and Periyar wildlife reserves.',
        'attractions': 'Alleppey Houseboats, Munnar Tea Gardens, Periyar Tiger Reserve, Varkala Cliff Beach, Fort Kochi Chinese Nets',
    },
    {
        'name': 'Shimla',
        'country': 'India',
        'category': 'Mountains',
        'image': '/static/images/shimla.svg',
        'description': 'The historic summer capital in the Himalayan foothills, renowned for UNESCO toy train rides, colonial architecture along The Ridge, and pine-draped hills.',
        'attractions': 'The Ridge & Mall Road, Kufri Snow Point, Jakhoo Hanuman Temple, Christ Church, Kalka-Shimla Toy Train',
    },
    {
        'name': 'Dubai',
        'country': 'United Arab Emirates',
        'category': 'Adventure',
        'image': '/static/images/dubai.svg',
        'description': 'A futuristic Arabian metropolis combining record-breaking skyscrapers, luxury desert safaris, dhow cruises, and world-class theme parks.',
        'attractions': 'Burj Khalifa 124th Floor, Arabian Desert Dune Bashing, Dubai Marina Dhow Cruise, Palm Jumeirah, Museum of the Future',
    },
    {
        'name': 'Bali',
        'country': 'Indonesia',
        'category': 'Honeymoon',
        'image': '/static/images/bali.svg',
        'description': 'The Island of the Gods offers volcanic rice terraces in Ubud, cliffside ocean temples at Uluwatu, turquoise Nusa Penida coves, and tranquil tropical villas.',
        'attractions': 'Uluwatu Sea Temple, Tegallalang Rice Terraces, Nusa Penida Kelingking Cliff, Sacred Monkey Forest, Seminyak Beach Club',
    },
    {
        'name': 'Ranthambore',
        'country': 'India',
        'category': 'Wildlife',
        'image': '/static/images/ranthambore.svg',
        'description': 'One of North India\'s premier national parks where Royal Bengal Tigers roam around ancient 10th-century hilltop fort ruins and deciduous jungle lakes.',
        'attractions': 'Ranthambore Tiger Safari Zones 1-5, Ranthambore Fort, Padam Talao Lake, Jogi Mahal, Kachida Valley',
    },
    {
        'name': 'Leh Ladakh',
        'country': 'India',
        'category': 'Adventure',
        'image': '/static/images/ladakh.svg',
        'description': 'High-altitude Trans-Himalayan desert renowned for crystalline alpine lakes, dramatic mountain passes, ancient Tibetan Buddhist monasteries, and expedition biking.',
        'attractions': 'Pangong Tso Lake, Nubra Valley Hunder Dunes, Khardung La Pass, Thiksey Monastery, Magnetic Hill',
    },
]

PACKAGES_DATA = [
    {
        'destination': 'Manali',
        'package_name': 'Himalayan Snow & Solang Adventure',
        'duration': '5 Days / 4 Nights',
        'price': 18500.00,
        'hotel_info': 'Snow Peak Mountain Chalet (4-Star) – Breakfast & Dinner included',
        'activities': 'Solang Paragliding, Atal Tunnel Drive, Hadimba Temple Walk, Old Manali Cafe Hopping, Beas River Rafting',
        'itinerary': 'Day 1: Arrival in Manali & Mall Road Evening Stroll | Day 2: Solang Valley Snow Sports & Atal Tunnel Excursion | Day 3: Hadimba Temple, Manu Temple & Vashisht Hot Springs | Day 4: Kullu River Rafting & Naggar Castle Heritage Tour | Day 5: Morning Pine Forest Walk & Departure',
        'availability': 'Available Daily (Nov 2026 - May 2027)',
        'description': 'Experience the magic of snow-draped Himachal peaks with guided excursions to Solang Valley, Rohtang foothills, and Kullu rafting rapids.',
    },
    {
        'destination': 'Manali',
        'package_name': 'Kullu-Manali Cozy Alpine Retreat',
        'duration': '4 Days / 3 Nights',
        'price': 14200.00,
        'hotel_info': 'Whispering Deodar Resort (3-Star Deluxe) – MAP Plan',
        'activities': 'Scenic Valley Drives, Apple Orchard Walk, Local Himachali Folk Dinner, Monastery Visit',
        'itinerary': 'Day 1: Check-in at Apple Orchard View Resort | Day 2: Solang Gondola & Snow Point | Day 3: Kullu Shawl Factory & Kasol Parvati Valley Day Trip | Day 4: Souvenir Shopping & Return Transfer',
        'availability': 'Available Daily (Year-Round)',
        'description': 'An affordable, relaxing mountain escape tailored for families and student groups looking for crisp mountain air and scenic valley trails.',
    },
    {
        'destination': 'Goa',
        'package_name': 'Goa Sun, Sand & Heritage Fiesta',
        'duration': '4 Days / 3 Nights',
        'price': 16800.00,
        'hotel_info': 'Marbella Beachfront Resort, Calangute (4-Star)',
        'activities': 'North Goa Beach Trail, Mandovi Sunset Cruise, Scuba & Jet Ski at Grande Island, Old Goa Churches',
        'itinerary': 'Day 1: Arrival at Dabolim/Mopa & Candolim Sunset Walk | Day 2: North Goa Forts (Aguada & Chapora) + Water Sports | Day 3: Old Goa UNESCO Basilica, Spice Plantation & Mandovi River Cruise | Day 4: Panjim Latin Quarter Walk & Departure',
        'availability': 'Available Daily (Oct 2026 - Apr 2027)',
        'description': 'Discover both vibrant North Goa beaches and tranquil South Goa Portuguese quarters with water sports and a sunset Mandovi cruise included.',
    },
    {
        'destination': 'Goa',
        'package_name': 'South Goa Luxury Palolem Escape',
        'duration': '5 Days / 4 Nights',
        'price': 24500.00,
        'hotel_info': 'Taj Exotica / Bay Suites South Goa (5-Star Luxury)',
        'activities': 'Private Catamaran Ride, Dudhsagar Waterfall Jeep Safari, Dolphin Spotting, Beachside Candlelight Dinner',
        'itinerary': 'Day 1: VIP Airport Pickup & Welcome Refreshments | Day 2: Palolem & Agonda Kayaking + Dolphin Excursion | Day 3: Dudhsagar Falls Safari & Sahakari Spice Tour | Day 4: Cabo de Rama Cliff Sunset & Private Dining | Day 5: Leisurely Breakfast & Departure',
        'availability': 'Available Thu-Sun (Nov 2026 - May 2027)',
        'description': 'Unwind on uncrowded crescent beaches in South Goa with boutique resort stays, spice tours, and private coastal dining.',
    },
    {
        'destination': 'Jaipur',
        'package_name': 'Royal Rajputana Pink City Heritage Tour',
        'duration': '3 Days / 2 Nights',
        'price': 11900.00,
        'hotel_info': 'Umaid Haveli Heritage Resort (4-Star)',
        'activities': 'Amber Fort Jeep Ascent, City Palace Guided Tour, Chokhi Dhani Cultural Dinner, Block Printing Workshop',
        'itinerary': 'Day 1: Arrival in Jaipur, Birla Mandir & Chokhi Dhani Village Feast | Day 2: Amber Fort, Jal Mahal, Hawa Mahal, Jantar Mantar & City Palace | Day 3: Nahargarh Fort Panorama, Sanganer Block Printing & Departure',
        'availability': 'Available Daily (Oct 2026 - Mar 2027)',
        'description': 'Step back into royal Rajasthani grandeur with curated palace tours, artisan workshops, and traditional Marwari hospitality.',
    },
    {
        'destination': 'Jaipur',
        'package_name': 'Golden Triangle Express: Jaipur, Agra & Delhi',
        'duration': '6 Days / 5 Nights',
        'price': 26900.00,
        'hotel_info': 'Heritage 4-Star Collection across Delhi, Agra & Jaipur',
        'activities': 'Sunrise Taj Mahal Tour, Fatehpur Sikri Visit, Amber Fort Sound & Light Show, Rickshaw Ride in Old Delhi',
        'itinerary': 'Day 1: New Delhi Monuments & India Gate | Day 2: Old Delhi Heritage & Express Drive to Agra | Day 3: Sunrise at Taj Mahal, Agra Fort & Fatehpur Sikri en route to Jaipur | Day 4: Amber Fort, City Palace & Jantar Mantar | Day 5: Nahargarh Sunset & Johari Bazaar | Day 6: Return to Delhi / Jaipur Airport Drop',
        'availability': 'Weekly Departures Every Monday & Friday',
        'description': 'India\'s signature cultural circuit connecting Delhi\'s historic landmarks, Agra\'s Taj Mahal, and Jaipur\'s majestic hilltop forts.',
    },
    {
        'destination': 'Kashmir',
        'package_name': 'Kashmir Paradise Houseboat & Gulmarg Odyssey',
        'duration': '6 Days / 5 Nights',
        'price': 28500.00,
        'hotel_info': '4 Nights Luxury Hotel + 1 Night Deluxe Dal Lake Houseboat',
        'activities': 'Private Dal Lake Shikara Ride, Gulmarg Gondola Phase 1, Pahalgam ABC Valley Excursion, Mughal Gardens Tour',
        'itinerary': 'Day 1: Srinagar Arrival & Evening Shikara Ride on Dal Lake | Day 2: Srinagar Mughal Gardens (Nishat, Shalimar, Chashme Shahi) | Day 3: Gulmarg Meadow of Flowers & Gondola Cable Car | Day 4: Drive to Pahalgam via Awantipora Ruins & Saffron Fields | Day 5: Betaab Valley & Aru Valley Excursion | Day 6: Wazwan Lunch & Srinagar Airport Transfer',
        'availability': 'Available Daily (Nov 2026 - Jun 2027)',
        'description': 'Indulge in timeless romance and alpine beauty with carved cedar houseboats, saffron valleys, and snow-covered Gulmarg slopes.',
    },
    {
        'destination': 'Kashmir',
        'package_name': 'Srinagar & Sonamarg Glacier Getaway',
        'duration': '4 Days / 3 Nights',
        'price': 19800.00,
        'hotel_info': 'Royal Heritage Houseboat & Boutique Hotel Srinagar',
        'activities': 'Thajiwas Glacier Pony Trail, Floating Vegetable Market Visit, Kashmiri Pashmina Artisans Tour',
        'itinerary': 'Day 1: Srinagar Houseboat Check-in & Sunset Shikara | Day 2: Full-Day Excursion to Sonamarg & Thajiwas Glacier | Day 3: Shankaracharya Hill, Hazratbal Shrine & Old City Walk | Day 4: Departure from Srinagar',
        'availability': 'Available Daily',
        'description': 'A compact Kashmir itinerary ideal for long weekends, combining Dal Lake houseboat charm with Sonamarg\'s alpine glaciers.',
    },
    {
        'destination': 'Kerala',
        'package_name': 'Munnar Misty Hills & Alleppey Backwater Bliss',
        'duration': '5 Days / 4 Nights',
        'price': 22400.00,
        'hotel_info': 'Munnar Tea Estate Resort + Private AC Deluxe Houseboat',
        'activities': 'Private Alleppey Backwater Cruise, Eravikulam National Park, Tea Museum Tasting, Kathakali Dance Performance',
        'itinerary': 'Day 1: Cochin Arrival & Scenic Drive to Munnar Waterfalls | Day 2: Mattupetty Dam, Echo Point, Tea Museum & Eravikulam Park | Day 3: Transfer to Thekkady Periyar Lake & Spice Walk | Day 4: Board Private Houseboat in Alleppey Backwaters | Day 5: Fort Kochi Heritage Tour & Airport Drop',
        'availability': 'Available Daily (Oct 2026 - May 2027)',
        'description': 'Sail tranquil palm-fringed canals on a private Kettuvallam houseboat after exploring Munnar\'s rolling emerald tea plantations.',
    },
    {
        'destination': 'Kerala',
        'package_name': 'Complete God\'s Own Country: Kochi to Kovalam',
        'duration': '7 Days / 6 Nights',
        'price': 31500.00,
        'hotel_info': '4-Star Eco Resorts & Beachfront Property in Kovalam',
        'activities': 'Periyar Wildlife Boating, Ayurvedic Rejuvenation Massage, Varkala & Kovalam Lighthouse Beaches',
        'itinerary': 'Day 1: Fort Kochi & Kathakali Show | Day 2: Munnar Tea Trails | Day 3: Munnar Top Station | Day 4: Thekkady Wildlife Sanctuary | Day 5: Alleppey Backwaters | Day 6: Kovalam Beach & Poovar Island | Day 7: Trivandrum Temple Visit & Departure',
        'availability': 'Weekly Departures',
        'description': 'The ultimate North-to-South Kerala journey spanning colonial Fort Kochi, highland tea estates, Periyar wildlife, and Arabian Sea cliffs.',
    },
    {
        'destination': 'Shimla',
        'package_name': 'Colonial Shimla & Kufri Toy Train Heritage',
        'duration': '4 Days / 3 Nights',
        'price': 13500.00,
        'hotel_info': 'Cedar Grand Heritage Hotel, Mall Road (4-Star)',
        'activities': 'UNESCO Kalka-Shimla Toy Train Ride, Kufri Himalayan Nature Park, Viceregal Lodge Guided Tour, Mall Road Walk',
        'itinerary': 'Day 1: Toy Train Arrival in Shimla & The Ridge Evening Promenade | Day 2: Kufri Fun World, Mahasu Peak & Fagu Valley | Day 3: Indian Institute of Advanced Study, Jakhoo Ropeway & Chadwick Falls | Day 4: Lakkar Bazaar Woodcraft Shopping & Return',
        'availability': 'Available Daily',
        'description': 'Relive timeless Himalayan hill-station charm with a UNESCO heritage rail journey, cedar trails, and panoramic snow viewpoints.',
    },
    {
        'destination': 'Dubai',
        'package_name': 'Dubai Skyline, Desert Safari & Marina Extravaganza',
        'duration': '5 Days / 4 Nights',
        'price': 54900.00,
        'hotel_info': 'Millennium Downtown / Business Bay Dubai (4-Star Superior)',
        'activities': 'Burj Khalifa At The Top, 4x4 Desert Dune Bashing & BBQ, Marina Luxury Dhow Dinner, Miracle Garden & Global Village',
        'itinerary': 'Day 1: Dubai International Arrival & Marina Dhow Cruise Dinner | Day 2: Half-Day Modern Dubai City Tour, Dubai Mall Aquarium & Burj Khalifa 124th Floor | Day 3: Afternoon Red Dunes Desert Safari with Belly Dance & Tanoura Show | Day 4: Palm Jumeirah Monorail, Atlantis View & Museum of the Future | Day 5: Gold & Spice Souk Creek Abra Ride & Airport Drop',
        'availability': 'Available Daily (Visa Assistance Available)',
        'description': 'Experience futuristic architectural marvels, golden desert dunes, and glittering marina cruises in the heart of the UAE.',
    },
    {
        'destination': 'Dubai',
        'package_name': 'Dubai & Abu Dhabi Grand Emirates Explorer',
        'duration': '6 Days / 5 Nights',
        'price': 68500.00,
        'hotel_info': '5-Star Sheikh Zayed Road Hotel with Daily International Buffet',
        'activities': 'Sheikh Zayed Grand Mosque, Ferrari World Yas Island, Burj Khalifa, Desert Camp, Dubai Frame',
        'itinerary': 'Day 1: Arrival & Dubai Frame Visit | Day 2: Burj Khalifa & Fountain Show | Day 3: Desert Safari Adventure | Day 4: Full-Day Abu Dhabi Grand Mosque & Ferrari World Tour | Day 5: Aquaventure Waterpark at Atlantis | Day 6: Duty-Free Shopping & Departure',
        'availability': 'Weekly Departures',
        'description': 'Combine the best of Dubai\'s iconic landmarks with a full-day excursion to Abu Dhabi\'s Sheikh Zayed Mosque and Yas Island.',
    },
    {
        'destination': 'Bali',
        'package_name': 'Tropical Bali: Ubud Rice Terraces & Nusa Penida Island',
        'duration': '6 Days / 5 Nights',
        'price': 48900.00,
        'hotel_info': 'Ubud Private Pool Villa (3N) + Seminyak Beach Resort (2N)',
        'activities': 'Nusa Penida Fast Boat Tour, Mount Batur Volcano View Lunch, Tegallalang Bali Swing, Uluwatu Kecak Fire Dance',
        'itinerary': 'Day 1: Denpasar Arrival & Transfer to Ubud Rainforest Villa | Day 2: Kintamani Volcano View, Tirta Empul Holy Spring & Tegallalang Swing | Day 3: Sacred Monkey Forest, Ubud Palace & Artisan Market | Day 4: Fast Boat to Nusa Penida (Kelingking Beach, Broken Beach & Crystal Bay) | Day 5: Tanah Lot & Uluwatu Cliff Temple with Kecak Sunset Dance | Day 6: Seminyak Cafe Breakfast & Airport Transfer',
        'availability': 'Available Daily (Visa on Arrival for Indian Passports)',
        'description': 'A curated tropical getaway pairing Ubud\'s lush jungle pool villas with the dramatic limestone cliffs of Nusa Penida and Uluwatu.',
    },
    {
        'destination': 'Ranthambore',
        'package_name': 'Ranthambore Royal Bengal Tiger Safari Expedition',
        'duration': '3 Days / 2 Nights',
        'price': 15400.00,
        'hotel_info': 'Sher Bagh / Tiger Machan Luxury Jungle Camp',
        'activities': '2 Confirmed Canter/Gypsy Jungle Safaris, Ranthambore Fort Trek, Naturalist Wildlife Talk, Bonfire Dinner',
        'itinerary': 'Day 1: Arrival at Sawai Madhopur, Resort Check-in & Afternoon Zone 3 Jungle Safari | Day 2: Early Morning Tiger Safari, Ranthambore Fort UNESCO Visit & Evening Wildlife Documentary | Day 3: Birdwatching Walk at Surwal Lake & Departure',
        'availability': 'Available Oct 2026 - Jun 2027',
        'description': 'Track the majestic Royal Bengal Tiger alongside expert naturalists across Ranthambore\'s scenic lakes and historic fort ruins.',
    },
    {
        'destination': 'Leh Ladakh',
        'package_name': 'Ladakh High Passes: Nubra Valley & Pangong Expedition',
        'duration': '6 Days / 5 Nights',
        'price': 34900.00,
        'hotel_info': 'Leh Boutique Hotel + Swiss Luxury Camps in Nubra & Pangong',
        'activities': 'Khardung La Pass (17,982 ft), Nubra Double-Humped Camel Safari, Pangong Lake Stargazing, Hemis & Thiksey Monasteries',
        'itinerary': 'Day 1: Arrival in Leh (Acclimatization) & Shanti Stupa Sunset | Day 2: Sham Valley Excursion (Hall of Fame, Magnetic Hill, Sangam Confluence) | Day 3: Drive via Khardung La Pass to Nubra Valley & Diskit Monastery | Day 4: Nubra to Pangong Tso Lake via Shyok River Route | Day 5: Sunrise at Pangong Lake, Chang La Pass & Thiksey Monastery | Day 6: Early Morning Scenic Flight from Leh',
        'availability': 'Available Apr - Oct Season',
        'description': 'Conquer the world\'s highest motorable passes and camp beside the color-changing waters of Pangong Tso in the Trans-Himalayas.',
    },
]


class Command(BaseCommand):
    help = 'Seeds Tourly database with 10 destinations, 16 tour packages, sample users, bookings, and contact messages.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Tourly database...")

        # 1. Create Admin & Demo Customer Users
        admin_user, created = User.objects.get_or_create(
            email='admin@tourly.com',
            defaults={
                'name': 'Aarav Sharma (Tourly Admin)',
                'phone': '+91-9876543210',
                'is_admin': True,
            }
        )
        if created:
            admin_user.set_password('Admin@123')
            admin_user.save()

        customer_user, created = User.objects.get_or_create(
            email='priya.verma@example.com',
            defaults={
                'name': 'Priya Verma',
                'phone': '+91-9811122334',
                'is_admin': False,
            }
        )
        if created:
            customer_user.set_password('Travel@123')
            customer_user.save()

        customer_two, created = User.objects.get_or_create(
            email='rohan.mehta@example.com',
            defaults={
                'name': 'Rohan Mehta',
                'phone': '+91-9822233445',
                'is_admin': False,
            }
        )
        if created:
            customer_two.set_password('Travel@123')
            customer_two.save()

        # 2. Seed Destinations
        dest_map = {}
        for d in DESTINATIONS_DATA:
            dest_obj, _ = Destination.objects.update_or_create(
                name=d['name'],
                defaults={
                    'country': d['country'],
                    'category': d['category'],
                    'image': d['image'],
                    'description': d['description'],
                    'attractions': d['attractions'],
                }
            )
            dest_map[d['name']] = dest_obj

        # 3. Seed Tour Packages
        pkg_objs = []
        for p in PACKAGES_DATA:
            dest_obj = dest_map[p['destination']]
            pkg_obj, _ = TourPackage.objects.update_or_create(
                package_name=p['package_name'],
                destination=dest_obj,
                defaults={
                    'duration': p['duration'],
                    'price': p['price'],
                    'image': dest_obj.image,
                    'hotel_info': p['hotel_info'],
                    'activities': p['activities'],
                    'itinerary': p['itinerary'],
                    'availability': p['availability'],
                    'description': p['description'],
                }
            )
            pkg_objs.append(pkg_obj)

        # 4. Seed Sample Bookings
        if Booking.objects.count() == 0 and len(pkg_objs) >= 4:
            Booking.objects.create(
                user=customer_user,
                package=pkg_objs[0],
                customer_name=customer_user.name,
                customer_email=customer_user.email,
                customer_phone=customer_user.phone,
                travel_date=date.today() + timedelta(days=21),
                travelers=2,
                total_price=float(pkg_objs[0].price) * 2,
                special_requirements='Mountain view balcony room preferred; vegetarian meals.',
                booking_status='Confirmed',
            )
            Booking.objects.create(
                user=customer_user,
                package=pkg_objs[6],
                customer_name=customer_user.name,
                customer_email=customer_user.email,
                customer_phone=customer_user.phone,
                travel_date=date.today() + timedelta(days=45),
                travelers=2,
                total_price=float(pkg_objs[6].price) * 2,
                special_requirements='Anniversary floral arrangement on Dal Lake houseboat.',
                booking_status='Pending',
            )
            Booking.objects.create(
                user=customer_two,
                package=pkg_objs[11],
                customer_name=customer_two.name,
                customer_email=customer_two.email,
                customer_phone=customer_two.phone,
                travel_date=date.today() + timedelta(days=30),
                travelers=4,
                total_price=float(pkg_objs[11].price) * 4,
                special_requirements='Require airport pickup for 4 adults with luggage.',
                booking_status='Confirmed',
            )

        # 5. Seed Sample Contact Messages
        if ContactMessage.objects.count() == 0:
            ContactMessage.objects.create(
                name='Ananya Nair',
                email='ananya.nair@example.com',
                phone='+91-9744556677',
                subject='Custom Group Quotation for Kerala Backwaters',
                message='Hello Tourly team, we are a group of 8 university faculty members planning a 5-day trip to Munnar and Alleppey in December. Could you share custom group discounts?',
            )
            ContactMessage.objects.create(
                name='Vikramaditya Singh',
                email='vikram.singh@example.com',
                phone='+91-9911223344',
                subject='Visa Assistance for Bali Honeymoon Package',
                message='We would like to book the 6-Day Tropical Bali package for January. Please confirm if airport fast-track Visa on Arrival guidance is included.',
            )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {Destination.objects.count()} destinations, "
            f"{TourPackage.objects.count()} tour packages, "
            f"{User.objects.count()} users, and {Booking.objects.count()} bookings."
        ))
