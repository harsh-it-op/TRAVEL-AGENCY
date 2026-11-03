#!/usr/bin/env python3
"""
TOURLY – Python CGI POST Request Demonstration (cgi/cgi_post.py)
Syllabus Requirement:
- Processing POST form data from standard input (`sys.stdin`) and `CONTENT_LENGTH`
- Handling user input safely and computing custom trip estimates
- Returning HTTP response headers and dynamic HTML output

Can be executed via CGI server or tested directly from terminal:
    echo "traveler_name=Priya+Verma&email=priya%40example.com&destination=Kashmir&travelers=3" | \
    REQUEST_METHOD="POST" CONTENT_LENGTH="79" python3 cgi/cgi_post.py
"""
import os
import sys
import html
from urllib.parse import parse_qs


BASE_FARES = {
    "Manali": 18500,
    "Goa": 16800,
    "Jaipur": 11900,
    "Kashmir": 28500,
    "Kerala": 22400,
    "Shimla": 13500,
    "Dubai": 54900,
    "Bali": 48900,
}


def read_post_payload():
    content_length_str = os.environ.get("CONTENT_LENGTH", "0").strip()
    try:
        length = int(content_length_str)
    except ValueError:
        length = 0

    if length > 0:
        raw_body = sys.stdin.read(length)
    else:
        raw_body = sys.stdin.read() if not sys.stdin.isatty() else ""
    return parse_qs(raw_body, keep_blank_values=True)


def main():
    method = os.environ.get("REQUEST_METHOD", "POST").upper()
    post_data = read_post_payload()

    traveler_name = html.escape(post_data.get("traveler_name", ["Guest Traveler"])[0].strip())
    email = html.escape(post_data.get("email", ["guest@tourly.com"])[0].strip())
    destination = html.escape(post_data.get("destination", ["Manali"])[0].strip())
    notes = html.escape(post_data.get("notes", ["Standard itinerary requested"])[0].strip())

    try:
        travelers = max(1, int(post_data.get("travelers", ["2"])[0]))
    except ValueError:
        travelers = 2

    unit_price = BASE_FARES.get(destination, 18500)
    total_estimate = unit_price * travelers

    # Output CGI HTTP Headers
    print("Content-Type: text/html; charset=utf-8")
    print("X-Powered-By: Tourly-Python-CGI/1.0")
    print()

    print(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tourly Python CGI – POST Form Quotation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="card shadow-sm border-0">
            <div class="card-header text-white py-3" style="background-color:#0A2540;">
                <h4 class="mb-0">Tourly Python CGI Demonstration – POST Request Processed ({method})</h4>
            </div>
            <div class="card-body p-4">
                <div class="alert alert-success">
                    <strong>Instant CGI Quotation Generated!</strong> Your POST payload was parsed and validated.
                </div>
                <ul class="list-group mb-3">
                    <li class="list-group-item d-flex justify-content-between">
                        <span>Lead Traveler Name:</span> <strong>{traveler_name}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        <span>Contact Email:</span> <strong>{email}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        <span>Selected Destination:</span> <strong>{destination} (&#8377;{unit_price:,} / person)</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        <span>Number of Travelers:</span> <strong>{travelers}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        <span>Special Notes:</span> <span>{notes}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between bg-light">
                        <span class="fw-bold">Total Estimated Package Cost:</span>
                        <strong class="text-danger fs-5">&#8377;{total_estimate:,}</strong>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>""")


if __name__ == "__main__":
    main()
