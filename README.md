# 🛒 Shop Web Application (Django + DRF + React)

> Full‑stack e‑commerce app with JWT auth, role‑based access, and an Amazon‑inspired UI.

**Backend:** Django · Django REST Framework · SimpleJWT  
**Frontend:** React (Vite) · React Router · Axios  
**Database:** SQLite for local dev · PostgreSQL‑ready for production (`DATABASE_URL`)

---

## ✨ Features

- 🔐 **JWT Authentication** (access + refresh tokens)
- 👑 **Roles**: Super Admin (Django superuser) and regular users
- 🛍️ **Product catalogue**
	- Product images
	- Discounts + final price calculation
	- Filters: Best sellers / New arrivals / Deals
	- Sorting by price and newest
	- Search (name + description)
- 🧺 **Shopping cart**
	- Add / remove products
	- Update quantity
	- Live totals and per‑item subtotals
- 📦 **Orders & checkout**
	- Create orders from the cart
	- Order history per user
	- Stock auto‑reduced via Django signals
- 🛠️ **Admin**
	- Django admin for products, discounts, orders
	- Super admin can view all orders
- 🧑 **Account page**
	- Update username, email, first & last name
	- Upload a **profile photo (avatar)**
- 💅 **Modern UI**
	- Amazon‑style product list and details
	- Responsive navbar, hero, product grid, cart and order cards

---

## 🗂 Project Structure

```text
shop_backend/
├─ config/              # Django project settings & URLs
├─ shop/                # E‑commerce app (models, views, serializers, signals)
├─ frontend/            # React + Vite application
├─ media/               # Uploaded media (product images, avatars)
├─ manage.py
├─ requirements.txt
└─ README.md
```

Key frontend folders (inside `frontend/src`):

- `pages/` – Product list & detail, Cart, Checkout, Orders, Account, Admin
- `components/` – Navbar, ProductCard, shared UI components
- `context/AuthContext.jsx` – JWT auth state and helpers
- `api/client.js` – Axios instance with auth header
- `styles/global.css` – Main styling

---

## ✅ Prerequisites

- Python 3.11+ (or compatible with your Django version)
- Node.js 18+ and npm
- (Optional) PostgreSQL if you want a production‑grade DB

---

## ⚙️ Backend Setup (Django + DRF)

From the project root:

```bash
cd shop_backend

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

### Environment variables (optional)

- `SECRET_KEY` – Django secret key (use a strong value in production)
- `DEBUG` – `"1"` for debug mode, anything else for False
- `DATABASE_URL` – e.g. `postgres://user:pass@host:5432/dbname`
- `FRONTEND_ORIGIN` – Frontend origin (default: `http://localhost:5173`)

Media (product images, avatars) is served from `/media/` in development.

### Seed sample products (with images)

Use the custom management command to seed the database with demo products and auto‑generated images:

```bash
python manage.py seed_products --count 20 --clear
```

Flags:

- `--count` – how many random products to create
- `--clear` – delete existing products before seeding

---

## 💻 Frontend Setup (React + Vite)

In a second terminal:

```bash
cd shop_backend/frontend

npm install
npm run dev
```

By default the app runs at `http://localhost:5173` and talks to the backend at `http://localhost:8000/api`.

You can override the API base URL using `VITE_API_BASE_URL` in a `.env` file in the `frontend` folder, e.g.:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🔑 Authentication & Roles

- JWT tokens are issued via SimpleJWT and stored in `localStorage` on the frontend.
- An Axios interceptor attaches `Authorization: Bearer <access>` to API calls.
- The logged‑in user is loaded from `/api/auth/me/` and stored in `AuthContext`.
- Super admin is any Django superuser; they can manage products and see all orders.

---

## 📡 Main API Endpoints

**Auth**

- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET  /api/auth/me/` – current user profile
- `GET  /api/auth/profile/` – current user profile (avatar)
- `PATCH /api/auth/profile/` – upload/update avatar

**Products**

- `GET  /api/products/` – list products (supports `filter`, `sort`, `q`)
- `GET  /api/products/{id}/` – product detail

**Cart**

- `GET  /api/cart/me/` – current user cart
- `POST /api/cart/add/` – add item (`product_id`, `quantity`)
- `POST /api/cart/remove/` – remove item (`product_id`)
- `POST /api/cart/update-quantity/` – update quantity (`product_id`, `quantity`)

**Orders**

- `GET  /api/orders/` – user: own orders; super admin: all orders
- `POST /api/orders/` – create order

**Admin**

- Standard Django admin at `/admin/` (use the superuser created earlier)

---

## 🚀 Running Everything Together

1. Start the Django backend:

	 ```bash
	 cd shop_backend
	 source .venv/bin/activate
	 python manage.py runserver 0.0.0.0:8000
	 ```

2. Start the React frontend in another terminal:

	 ```bash
	 cd shop_backend/frontend
	 npm run dev
	 ```

3. Open the app in the browser at `http://localhost:5173`.

4. Log in with the superuser credentials to access admin features, or register a new user from the UI.

---

## 📝 Notes

- This is a demo / starter project, not a production‑hardened store.
- For deployment, you would typically:
	- Switch to PostgreSQL via `DATABASE_URL`
	- Serve the built React app (`npm run build`) behind a web server
	- Configure static/media hosting and HTTPS

Feel free to fork and adapt it for your own learning or projects.
