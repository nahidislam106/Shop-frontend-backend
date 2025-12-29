# Shop Web Application (Django + React)

Backend: Django + DRF + SimpleJWT
Frontend: React (Vite) + Axios
Database: SQLite (local) / PostgreSQL (production via `DATABASE_URL`).

## Backend Setup

```bash
cd "new folder/shop_backend"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Environment variables (optional):
- `SECRET_KEY`
- `DEBUG` ("1" for True)
- `DATABASE_URL` (e.g., `postgres://user:pass@host:5432/dbname`)
- `FRONTEND_ORIGIN` (default `http://localhost:5173`)

## Frontend Setup

```bash
cd "new folder/shop_backend/frontend"
npm install
npm run dev
```

## Main API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`
- `GET /api/products/` (public)
- `GET /api/products/{id}/` (public)
- `GET /api/cart/me/` (auth)
- `POST /api/cart/add/` (auth)
- `POST /api/cart/remove/` (auth)
- `POST /api/cart/update-quantity/` (auth)
- `GET /api/orders/` (user: own orders, super admin: all orders)
- `POST /api/orders/` (auth)

Super Admin is the Django superuser and has full CRUD on products and orders via the admin site and APIs.
