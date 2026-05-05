# Coderr Backend

Coderr Backend is a Django REST Framework API for a freelancer platform.

It provides authentication, profiles, offers, orders, reviews and platform statistics for the Coderr frontend.

## Tech Stack

- Python
- Django
- Django REST Framework
- Token Authentication
- django-filter
- django-cors-headers
- SQLite for local development

## Project Structure

```text
coderr_backend/
├── auth_app/
├── profiles_app/
├── offers_app/
├── orders_app/
├── reviews_app/
├── base_info_app/
├── core/
├── manage.py
├── requirements.txt
└── README.md
```


## Setup

### 1. Clone the repository

```bash
git clone https://github.com/DennisDumin/coderr_backend.git
cd coderr_backend
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv env
env\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The backend runs at:

```text
http://127.0.0.1:8000/
```

The API base URL is:

```text
http://127.0.0.1:8000/api/
```

## Frontend Connection

The Coderr frontend expects the backend here:

```text
http://127.0.0.1:8000/api/
```

CORS is enabled for local development.

## Authentication

The API uses DRF Token Authentication.

Authenticated requests need this header:

```text
Authorization: Token <your-token>
```

## Guest Users

The frontend contains these guest login credentials:

```text
Customer:
username: andrey
password: asdasd

Business:
username: kevin
password: asdasd24
```

These users must exist in the local database before using the guest login.
They can be created through the registration endpoint or Django admin.

## Main Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/registration/` | Register a customer or business user | No |
| POST | `/api/login/` | Login and receive token | No |

### Profiles

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/profile/{id}/` | Get a user profile | Yes |
| PATCH | `/api/profile/{id}/` | Update own profile | Yes |
| GET | `/api/profiles/business/` | List business profiles | Yes |
| GET | `/api/profiles/customer/` | List customer profiles | Yes |

### Offers

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/offers/` | List offers | No |
| POST | `/api/offers/` | Create offer with 3 details | Business only |
| GET | `/api/offers/{id}/` | Get one offer | Yes |
| PATCH | `/api/offers/{id}/` | Update own offer | Owner only |
| DELETE | `/api/offers/{id}/` | Delete own offer | Owner only |
| GET | `/api/offerdetails/{id}/` | Get one offer detail | Yes |

Supported offer query parameters:

```text
creator_id
min_price
max_delivery_time
ordering
search
page
page_size
```

Each offer must contain exactly three offer details:

```text
basic
standard
premium
```

### Orders

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/orders/` | List own related orders | Yes |
| POST | `/api/orders/` | Create order from offer detail | Customer only |
| PATCH | `/api/orders/{id}/` | Update order status | Business owner only |
| DELETE | `/api/orders/{id}/` | Delete order | Admin only |
| GET | `/api/order-count/{business_user_id}/` | Count active business orders | Yes |
| GET | `/api/completed-order-count/{business_user_id}/` | Count completed business orders | Yes |

Order status values:

```text
in_progress
completed
cancelled
```

### Reviews

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/reviews/` | List reviews | Yes |
| POST | `/api/reviews/` | Create review | Customer only |
| PATCH | `/api/reviews/{id}/` | Update own review | Owner only |
| DELETE | `/api/reviews/{id}/` | Delete own review | Owner only |

Supported review query parameters:

```text
business_user_id
reviewer_id
ordering
```

### Base Info

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/base-info/` | Get platform statistics | No |

Response contains:

```json
{
  "review_count": 0,
  "average_rating": 0,
  "business_profile_count": 0,
  "offer_count": 0
}
```

## Media Files

Uploaded profile and offer images are served from:

```text
/media/
```

During development Django serves media files automatically when `DEBUG=True`.

## Database

The local SQLite database file `db.sqlite3` is ignored by Git and must not be uploaded to GitHub.

To recreate the database on another machine:

```bash
python manage.py migrate
```

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Notes

- The backend repository contains no frontend code.
- The API is built for the existing Coderr frontend.
- Frontend repository: https://github.com/Developer-Akademie-Backendkurs/project.Coderr
- All endpoints are available without rate limiting.
- All API endpoints use trailing slashes.
