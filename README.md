# MilkMan Full Stack

MilkMan is a dairy product subscription and one-time order ecommerce system.

## Repositories in this workspace
- `backend/`: Django + DRF + JWT API
- `frontend/`: React + Tailwind web app

## Quick start
1. Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_milkman
   python manage.py runserver
   ```
2. Frontend (new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Frontend URL: `http://localhost:5173`  
Backend URL: `http://127.0.0.1:8000`

## Demo login credentials
- Admin: `ankits@gmail.com` / `ankit@123`
- Customer: `customer1@test.com` / `strongpassword123`
