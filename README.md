# 🥛 MilkMan Full Stack

MilkMan is a dairy product subscription and one-time order ecommerce system built with Django and React. Customers can subscribe to daily or weekly dairy products, manage orders, and track payments, while admins can manage products, monitor subscriptions, and analyze revenue from a structured dashboard.

---

## 📂 Repositories in this workspace

- `backend/` → Django + DRF + JWT API  
- `frontend/` → React + Tailwind web app  

---

## 🚀 Quick Start

### 1️⃣ Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_milkman
python manage.py runserver
```

### 2️⃣ Frontend (Open New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: http://localhost:5173  
Backend URL: http://127.0.0.1:8000  

---

## 🔐 Demo Login Credentials

**Admin**  
Email: ankits@gmail.com  
Password: ankit@123  

**Customer**  
Email: customer1@test.com  
Password: strongpassword123  

---

# 📸 Application Screenshots

⚠️ Create a folder named `screenshots` in the root directory and place your images inside it.

---

## 🏠 Home Page

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/c6a75cfb-dd46-42c9-bce1-e30ef18b8fdd" />


---

## 🥛 Dairy Products Page

<img width="1895" height="1079" alt="image" src="https://github.com/user-attachments/assets/b2376c9f-4783-4bf0-9920-080f3672a420" />


---

## 🔁 Subscription Plans Page

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/32af1557-efaf-40c7-9da2-81569858411e" />


---

## 📊 Admin Dashboard

<img width="1885" height="1079" alt="image" src="https://github.com/user-attachments/assets/bafff614-e738-469a-a2b5-3a8e934f1e20" />


---

## ➕ Admin Add Product (Reflects on Home Page)

<img width="1228" height="366" alt="image" src="https://github.com/user-attachments/assets/41b76711-04ca-4311-9696-99848f3f3bb2" />


---

## 👤 Customer Profile

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/98a57c89-c7a7-492d-9491-d1368b19b032" />


---

# 🛠 Tech Stack

Backend:
- Django
- Django REST Framework
- SimpleJWT

Frontend:
- React
- Tailwind CSS
- Axios

---

# 🎯 Core Features

- Role based authentication (Admin & Customer)
- JWT login system
- Daily & Weekly subscription model
- Pause / Resume subscription
- One-time product ordering
- Admin analytics dashboard
- Product demand tracking
- Revenue monitoring
- Clean scalable backend architecture

---

# 📌 Project Purpose

MilkMan simulates a real-world dairy delivery system where customers manage recurring milk and dairy subscriptions while administrators control products, pricing, and business analytics from a centralized dashboard.
