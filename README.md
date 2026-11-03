# Tourly – Full-Stack Travel Agency Management and Booking System

Tourly is a responsive, database-driven Travel Agency Website developed strictly according to the **University Web Technologies Syllabus**. It features two full-fledged interfaces (**Customer Website** and **Administrator Dashboard**) powered by **Django MVT Architecture** and **MySQL**, alongside interactive frontend modules in **HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, jQuery AJAX, and AngularJS**, plus standalone academic demonstrations for **Python CGI** and **Node.js**.

---

## 1. Syllabus Technology Mapping (Where Every Technology Is Used)

| Syllabus Technology | Exact Files in Project | Features Demonstrated |
| :--- | :--- | :--- |
| **HTML5** | `templates/*.html` (12 templates) | Semantic `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, HTML5 forms, date pickers, modals, and tables |
| **CSS3 (External, Internal, Inline)** | External: `static/css/style.css`<br>Internal: `<style>` block in `templates/base.html`<br>Inline: `style="..."` on navbar brand & banners | Custom CSS variables (`--tourly-navy: #0A2540`, `--tourly-turquoise: #00B4D8`, `--tourly-orange: #FF6B35`), card hover scale transitions, status badges |
| **JavaScript (ES6 DOM & Events)** | `static/js/script.js` | Registration & Booking form validation, password visibility toggle (`Show/Hide`), live traveler count stepper & dynamic total price calculation, image gallery switcher, custom toast notifications |
| **Bootstrap 5.3** | All templates in `templates/` | Responsive 12-column grid, sticky mobile navbar, destination/package cards, quick-view modals, admin tabs, status badges |
| **jQuery 3.7 & AJAX (JSON)** | `static/js/jquery-functions.js` + `travel/views.py` (`api_*` views) | Live destination search without page reload, multi-criteria tour package filtering, asynchronous package quick-view modal, AJAX Contact Us submission with CSRF token, dynamic Admin booking status updates |
| **AngularJS 1.8** | `static/js/angular-app.js` + `templates/home.html` & `templates/booking.html` | Configured with `[[ ]]` interpolation to coexist cleanly with Django `{{ }}`; `DestinationExplorerController` (live two-way bound filtering & cost estimator) and `TripCalculatorController` (dynamic companion manifest & add-on calculator) |
| **Python & Django MVT** | `tourly_project/`, `travel/models.py`, `travel/views.py`, `travel/urls.py`, `travel/forms.py` | Complete MVT architecture, session authentication, PBKDF2 password hashing, protected customer/admin decorators, dynamic URL routing |
| **MySQL & Django ORM** | `sql/schema.sql`, `travel/models.py`, `travel/migrations/0001_initial.py` | 5 relational tables (`Users`, `Destinations`, `TourPackages`, `Bookings`, `ContactMessages`) with Foreign Keys (`ON DELETE CASCADE`) and indexes |
| **MySQL Connector/Python** | `sql/mysql_connector_demo.py` | Standalone Python database connectivity demonstration executing parameterized `SELECT`, `INNER JOIN`, and `GROUP BY` queries |
| **Python CGI (GET & POST)** | `cgi/cgi_get.py`, `cgi/cgi_post.py` | Standalone CGI scripts parsing `QUERY_STRING` (GET) and `sys.stdin` / `CONTENT_LENGTH` (POST), emitting HTTP headers and HTML5 responses |
| **Node.js Server** | `node/node_server.js` | Standalone lightweight HTTP server using Node's native `http` and `url` modules (no Express) serving JSON on `/status`, `/api/advisories`, and `/api/currency` |

---

## 2. Project Directory Structure

```text
Tourly/
├── manage.py
├── requirements.txt
├── README.md
├── tourly_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── travel/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/commands/seed_tourly.py
│   └── migrations/0001_initial.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── destinations.html
│   ├── destination_detail.html
│   ├── packages.html
│   ├── package_details.html
│   ├── booking.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin_dashboard.html
│   └── contact.html
├── static/
│   ├── css/style.css
│   ├── js/
│   │   ├── script.js
│   │   ├── jquery-functions.js
│   │   └── angular-app.js
│   └── images/ (11 high-resolution SVG travel illustrations)
├── sql/
│   ├── schema.sql
│   └── mysql_connector_demo.py
├── cgi/
│   ├── cgi_get.py
│   └── cgi_post.py
├── node/
│   └── node_server.js
└── screenshots/
    ├── 01_homepage.png
    ├── 02_destinations_and_packages.png
    ├── 03_booking_and_angularjs.png
    ├── 04_customer_dashboard.png
    └── 05_admin_dashboard.png
```

---

## 3. Step-by-Step Setup & Installation Instructions

### Step 1: Create Virtual Environment & Install Dependencies
```bash
cd Tourly
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure MySQL Database
1. Log into your local MySQL Server and execute the schema script:
```bash
mysql -u root -p < sql/schema.sql
```
2. Set your MySQL credentials via environment variables (or edit `tourly_project/settings.py`):
```bash
export MYSQL_DATABASE="tourly_db"
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_mysql_password"
export MYSQL_HOST="127.0.0.1"
export MYSQL_PORT="3306"
```
*(Tip: For quick offline testing on a laptop without MySQL Server running, set `export TOURLY_USE_SQLITE=True`)*

### Step 3: Run Migrations & Seed 10 Destinations + 16 Tour Packages
```bash
python3 manage.py migrate
python3 manage.py seed_tourly
```

### Step 4: Start the Django Application Server
```bash
python3 manage.py runserver 8000
```
Open **`http://127.0.0.1:8000/`** in your browser.

---

## 4. Default Login Credentials (Seeded by `seed_tourly`)

| Role | Email Address | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@tourly.com` | `Admin@123` | Full access to `/admin-dashboard/` (CRUD for Destinations, Packages, Bookings, Users, Contact Messages) |
| **Customer 1** | `priya.verma@example.com` | `Travel@123` | Access to `/dashboard/`, booking history, upcoming trips, and booking cancellation |
| **Customer 2** | `rohan.mehta@example.com` | `Travel@123` | Access to `/dashboard/` with sample Dubai family booking |

---

## 5. Testing Instructions for All Syllabus Modules

### A. Run Automated Django Unit & Integration Tests
```bash
TOURLY_USE_SQLITE=True python3 manage.py test
```

### B. Test MySQL Connector/Python Script
```bash
python3 sql/mysql_connector_demo.py
```

### C. Test Python CGI GET & POST Scripts
```bash
# Test CGI GET Request Handler:
QUERY_STRING="destination=Manali&category=Mountains&budget=25000" python3 cgi/cgi_get.py

# Test CGI POST Request Handler:
echo "traveler_name=Priya+Verma&email=priya%40example.com&destination=Kashmir&travelers=3&notes=Houseboat+suite" | \
REQUEST_METHOD="POST" CONTENT_LENGTH="104" python3 cgi/cgi_post.py
```
Or serve them over HTTP using Python's built-in CGI HTTP server:
```bash
python3 -m http.server --cgi 8080
# Visit: http://127.0.0.1:8080/cgi/cgi_get.py?destination=Goa&budget=20000
```

### D. Test Standalone Node.js Micro-Server
```bash
node node/node_server.js
```
Then open another terminal or browser and test:
- `http://127.0.0.1:4000/status` — Server health & uptime JSON
- `http://127.0.0.1:4000/api/advisories?destination=Manali` — Travel weather & highway status JSON
- `http://127.0.0.1:4000/api/currency?inr=18500` — Live INR to USD/AED/EUR conversion JSON
