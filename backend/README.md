# MilkMan Backend

Production-ready Django REST backend for a dairy product subscription ecommerce system.

## Stack
- Django
- Django REST Framework
- SimpleJWT authentication
- PostgreSQL-ready settings
- Custom user model with roles (`ADMIN`, `CUSTOMER`)

## App structure
```text
backend/
  milkman_backend/
  users/
  products/
  subscriptions/
  cart/
  payments/
  analytics/
  fixtures/
```

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   ```bash
   DJANGO_SECRET_KEY=replace-this
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

   # PostgreSQL (optional)
   DB_ENGINE=django.db.backends.postgresql
   POSTGRES_DB=milkman_db
   POSTGRES_USER=milkman_user
   POSTGRES_PASSWORD=milkman_pass
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Seed demo users + products:
   ```bash
   python manage.py seed_milkman
   ```
6. (Optional) Load fixture-only product data:
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```
7. Run server:
   ```bash
   python manage.py runserver
   ```

## Production on a VM
- Copy `backend/.env.example` to `backend/.env` and replace the placeholder values.
- Use `gunicorn.conf.py` with Gunicorn on Linux:
  ```bash
  gunicorn --config gunicorn.conf.py milkman_backend.wsgi:application
  ```
- For an Azure VM deployment with Nginx and systemd, use the files in `deploy/azure-vm/`.

## Demo credentials
- Admin (superuser):
  - Email: `ankits@gmail.com`
  - Password: `ankit@123`
- Customer:
  - Email: `customer1@test.com`
  - Password: `strongpassword123`

## Authentication behavior
- Login: `POST /api/auth/login/`
- Refresh: `POST /api/auth/token/refresh/`
- Register: `POST /api/auth/register/`
- Profile: `GET/PATCH /api/auth/profile/`

Login response includes:
- `access`
- `refresh`
- `user`
- `redirect_to`
  - `/admin-dashboard` for superuser
  - `/customer-dashboard` for customer

## API routes

### Products
- `GET /api/products/items/`
- `GET /api/products/items/{id}/`
- `POST /api/products/items/` (Admin)
- `PATCH /api/products/items/{id}/increase_price/` (Admin)
- `GET /api/products/categories/`

### Subscriptions
- `GET /api/subscriptions/`
- `POST /api/subscriptions/` (Customer)
- `POST /api/subscriptions/bulk_subscribe/` (Customer, up to 5 products)
- `PATCH /api/subscriptions/{id}/pause/`
- `PATCH /api/subscriptions/{id}/resume/`
- `PATCH /api/subscriptions/{id}/cancel/`
- `GET /api/subscriptions/{id}/history/`
- `GET /api/subscriptions/admin_overview/` (Admin)

### Cart and One-Time Orders
- `GET /api/cart/`
- `POST /api/cart/items/`
- `PATCH /api/cart/items/{item_id}/`
- `DELETE /api/cart/items/{item_id}/`
- `POST /api/cart/checkout/` (creates one-time order + payment)
- `GET /api/cart/orders/`

### Payments
- `GET /api/payments/`
- `POST /api/payments/`
- `PATCH /api/payments/{id}/update_status/` (Admin)

### Analytics (Admin)
- `GET /api/analytics/dashboard/`
- `GET /api/analytics/product-demand/`
- `GET /api/analytics/subscription-growth/`

## Database schema (high level)
- `users_user`: custom user with email login and role.
- `products_category`: product categories.
- `products_product`: product catalog with stock, unit, demand count, image URL.
- `subscriptions_subscription`: customer subscriptions with frequency (`DAILY`, `WEEKLY`) and total price calculation.
- `subscriptions_subscriptionhistory`: status change tracking.
- `cart_cart` + `cart_cartitem`: one-time order cart (max 5 unique products).
- `cart_onetimeorder` + `cart_onetimeorderitem`: finalized one-time orders.
- `payments_payment`: payment records linked to subscription or one-time order.

## Business rules implemented
- Demand count increments via subscription signal.
- Low stock warning is exposed in product serializer.
- Product auto marked unavailable when stock reaches `0`.
- Subscription creation prevented when product is unavailable/out of stock.
- One-time cart limits to 5 unique products.
- Revenue analytics computed from successful payments.
- Role-based API protection for admin/customer routes.
