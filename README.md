# 🏠 Household Service Platform

A comprehensive online platform connecting homeowners with professionals for household services such as cleaning, plumbing, electrical work, lawn care, pest control, painting, and home repairs.

---

## 🚀 Demo

- **Preview Video**: [Watch here](https://drive.google.com/file/d/1OozakE-Dj72zDOwhWzIx2_azcFoEfMJq/view?usp=drive_link)  
- **Documentation**: [View Documentation](https://drive.google.com/file/d/1DE2eKkshxdzDvEQlID5JdukZSG6o6D2a/view?usp=sharing)

---

## ⏳ Installation and Setup

### 📁 1. Clone the Repository

```bash
git clone https://github.com/Jatinbhardwaj-093/HouseHold-Service-Platform.git
```

### 📂 2. Navigate to the Project Directory

```bash
cd HouseHold-Service-Platform
```
## Backend

### 🖥️ 3. Create and Activate a Virtual Environment
- **Create Venv**
```bash
cd backend
python -m venv venv
```

- **Activate Virtual Environment**
  
  **For Linux/macOS**
  ```bash
  source venv/bin/activate
  ```
  **For Windows**
  ```bash
  venv\\Scripts\\activate
  ```

### 🔧 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### ▶️ 5. Start the Backend Server
```bash
python app.py
```
  **OR**
```bash
flask run
```

### ⚙️ 6. Setup Redis
Ensure Redis is installed. Start Redis with:
```bash 
redis-server
```

### 🛠️ 7. Run Celery Worker
In a new terminal window,run the Celery worker:
```bash 
cd ../backend
celery -A app.celery worker
```

### 🕐 8. Run Celery Beat
In a new terminal window,run the Celery beat:
```bash 
cd ../backend
celery -A app.celery beat
```

## Frontend

### 📥 9. Install Frontend Dependices
In a new terminal window,run the Celery beat:
```bash
cd ../frontend
npm install
```

### ▶️ 10. Run Frontend Development server

```bash
npm run dev
```
## 👨🏻‍💼 Create an Admin User

To set up an admin user for monitoring and control, run the following:

```bash
cd ../backend
python create_admin.py
```

**Note:** Update the credentials in the create_admin.py file as needed.

## ✍🏻Author

- [@Github-JatinBhardwaj](https://github.com/Jatinbhardwaj-093)
- [@LinkedIn-JatinBhardwaj](https://www.linkedin.com/in/jatin-bhardwaj-b5962921a/)
