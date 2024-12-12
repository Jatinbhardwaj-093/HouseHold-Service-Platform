
# 🏠Household Service Platform

A household service website is an online platform that connects homeowners with professionals or businesses offering various household services. These services typically include cleaning, plumbing, electrical work, lawn care, pest control, painting, home repairs, and other maintenance or improvement tasks.



## Demo

#### 📽️Preview video
https://drive.google.com/file/d/1OozakE-Dj72zDOwhWzIx2_azcFoEfMJq/view?usp=drive_link

#### 📄Documentation
https://drive.google.com/file/d/1DE2eKkshxdzDvEQlID5JdukZSG6o6D2a/view?usp=sharing



# ⏳Installation and SetUp

### 1. Clone the Reposistory

```bash
git clone https://github.com/Jatinbhardwaj-093/HouseHold-Service-Platform.git
```

### 2.Change the working directory

```bash
cd HomeService
```
## Backend

### 3. Create & activate Virtual Environment
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

### 4. Install Backend Dependices

```bash
pip install -r requirements.txt
```

### 5.Start the backend server

```bash
python run.py
```
     
  **or**

```bash
flask run
```

### 6. Setup Redis
Make sure Redis is installed and running. 
You can start Redis using:
```bash 
redis-server
```

### 7. Run Celery Worker
In a new terminal window,run the Celery worker:
```bash 
cd ../backend
celery -A app.celery worker
```

### 8. Run Celery Beat
In a new terminal window,run the Celery beat:
```bash 
cd ../backend
celery -A app.celery beat
```

## Frontend

### 9. Install Frontend Dependices
In a new terminal window,run the Celery beat:
```bash
cd ../frontend
npm install
```

### 10. Run Frontend Development server

```bash
npm run dev
```
## ✍🏻Author

- [@Github-JatinBhardwaj](https://github.com/Jatinbhardwaj-093)
- [@LinkedIn-JatinBhardwaj](https://www.linkedin.com/in/jatin-bhardwaj-b5962921a/)
