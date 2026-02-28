# MilkMan Frontend

React + Tailwind UI for MilkMan dairy subscription ecommerce.

## Stack
- React
- React Router
- Axios
- Tailwind CSS
- Context API (`AuthContext`, `ToastContext`)

## Run
```bash
npm install
npm run dev
```

Optional environment:
```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Core Pages
- `/` Home
- `/products` Dairy products list + subscribe modal
- `/subscription-plans` Plan information
- `/admin-dashboard` Admin-only dashboard
- `/customer-dashboard` Customer-only dashboard
- `/cart` One-time order cart checkout
- `/payment` Payment history and updates

## Authentication behavior
- JWT stored in `localStorage`
- Superuser redirect: `/admin-dashboard`
- Customer redirect: `/customer-dashboard`
- If unauthenticated, home page is default
- Login/Register uses modal popup
