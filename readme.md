# 📚 Library Management System

This project is a **Library Management System** developed using **Streamlit (Python)** for the frontend and **Node.js (JavaScript)** for the backend.

## 🛠 Technologies Used

### Frontend

- Python
- Streamlit
- Pandas
- Requests

### Backend

- Node.js
- Express
- TypeScript
- Database (for user authentication only)
- CSV files (for book management)

---

## 🗄️ Database Setup (Required Once)

The database is required **only for user login**.

### Step 1: Create Database

Create an empty database in your system.

Example (MySQL):

```sql
CREATE DATABASE library;

### Backend Setup
cd backend
npm install
npm run dev

### Frontend Setup
cd frontend
pip install streamlit pandas requests
streamlit run app.py
```
