#!/usr/bin/env python3
"""
TOURLY – Python CGI GET Request Demonstration (cgi/cgi_get.py)
Syllabus Requirement:
- Reading GET parameters from QUERY_STRING / urllib.parse
- Handling user input safely with HTML escaping
- Returning appropriate HTTP headers (`Content-Type: text/html; charset=utf-8`)
- Generating a complete, responsive HTML5 response

Can be executed via CGI web server or tested directly from terminal:
    QUERY_STRING="destination=Manali&category=Mountains&budget=25000" python3 cgi/cgi_get.py
"""
import os
import html
from urllib.parse import parse_qs


CATALOG = [
    {"name": "Manali", "category": "Mountains", "price": 18500, "duration": "5 Days / 4 Nights"},
    {"name": "Goa", "category": "Beaches", "price": 16800, "duration": "4 Days / 3 Nights"},
    {"name": "Jaipur", "category": "Historical Places", "price": 11900, "duration": "3 Days / 2 Nights"},
    {"name": "Kashmir", "category": "Honeymoon", "price": 28500, "duration": "6 Days / 5 Nights"},
    {"name": "Kerala", "category": "Wildlife", "price": 22400, "duration": "5 Days / 4 Nights"},
    {"name": "Dubai", "category": "Adventure", "price": 54900, "duration": "5 Days / 4 Nights"},
]


def main():
    raw_query = os.environ.get("QUERY_STRING", "")
    params = parse_qs(raw_query, keep_blank_values=True)

    destination = html.escape(params.get("destination", [""])[0].strip())
    category = html.escape(params.get("category", [""])[0].strip())
    budget_str = html.escape(params.get("budget", ["60000"])[0].strip())

    try:
        max_budget = float(budget_str) if budget_str else 60000.0
    except ValueError:
        max_budget = 60000.0

    filtered = []
    for item in CATALOG:
        if destination and destination.lower() not in item["name"].lower():
            continue
        if category and category.lower() != item["category"].lower():
            continue
        if item["price"] > max_budget:
            continue
        filtered.append(item)

    # Emit HTTP Headers required by CGI specification
    print("Content-Type: text/html; charset=utf-8")
    print("X-Powered-By: Tourly-Python-CGI/1.0")
    print()  # Blank line separating headers from body

    rows_html = ""
    for item in filtered:
        rows_html += (
            f"<tr>"
            f"<td><strong>{item['name']}</strong></td>"
            f"<td><span class='badge bg-info text-dark'>{item['category']}</span></td>"
            f"<td>{item['duration']}</td>"
            f"<td>&#8377;{item['price']:,}</td>"
            f"</tr>"
        )
    if not rows_html:
        rows_html = "<tr><td colspan='4' class='text-center text-muted'>No packages matched the GET parameters.</td></tr>"

    print(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tourly Python CGI – GET Request Handler</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="card shadow-sm border-0">
            <div class="card-header text-white py-3" style="background-color:#0A2540;">
                <h4 class="mb-0">Tourly Python CGI Demonstration – GET Request Processing</h4>
            </div>
            <div class="card-body p-4">
                <p class="text-muted">
                    This standalone CGI script reads URL query parameters from <code>os.environ['QUERY_STRING']</code>
                    and dynamically filters the Tourly destination catalog.
                </p>
                <div class="alert alert-info">
                    <strong>Parsed GET Parameters:</strong>
                    Destination = <code>{destination or 'All'}</code> |
                    Category = <code>{category or 'All'}</code> |
                    Max Budget = <code>&#8377;{max_budget:,.2f}</code>
                </div>
                <table class="table table-bordered table-striped align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th>Destination</th>
                            <th>Category</th>
                            <th>Duration</th>
                            <th>Starting Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>""")


if __name__ == "__main__":
    main()
