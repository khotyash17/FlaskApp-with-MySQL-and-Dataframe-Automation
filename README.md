# 📚 Student Registration System with CSV Exporter  

This project is a **Dockerized Flask Web Application** integrated with **MySQL** for storing student registration data. It also includes a **CSV Exporter service** that automatically extracts student data from the MySQL database and saves it into CSV files for easy reporting and analysis.  

---
## 🚀 Features  
- 🖥️ **Flask Web App** – Register and manage student data through a simple UI.  
- 🗄️ **MySQL Database** – Persistent storage of student details.  
- 🐳 **Docker Compose Setup** – Multi-container setup (Flask, MySQL, Exporter).  
- 📤 **CSV Export Automation** – Export student records into timestamped CSV files.  
- 🔗 **Custom Networking** – Containers communicate seamlessly via Docker bridge network.  

---

## 🛠️ Tech Stack  
- **Flask (Python)** – Backend web framework  
- **MySQL** – Relational database  
- **Docker & Docker Compose** – Containerization & orchestration  
- **Shell Scripting** – Automated CSV export  

---
## 📂 Project Structure 
project-root/ <br>
│── app.py # Flask web application / <br>
│── requirements.txt # Python dependencies / <br>
│── Dockerfile # Flask app Dockerfile <br>
│── docker-compose.yml # Multi-container setup <br>
│── mysql-init/ # Auto-init SQL scripts for DB & table <br>
│── corn/ # CSV exporter service <br>
│ ├── Dockerfile <br>
│ ├── export.sh # Export script <br>
│── exports/ # CSV files will be saved here <br>

---

## ⚡ Setup Instructions  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/student-registration-system.git
cd student-registration-system
```
2️⃣ Build & Start Containers
```
docker compose up -d --build
```
3️⃣ Access the Flask App
```
Open browser → http://localhost:5000
```
Register students via the form

4️⃣ Export Data to CSV
```
docker exec -it csv-exporter sh /app/export.sh
```
- Exported CSV files will appear in the exports/ folder

📊 Example CSV Output
```
id,name,email,created_at
1,Testing,test@example.com
```
✅ Improvements (Future Scope)
```
Add authentication for secure access
Automate CSV export with cron jobs
Add Docker volume for log management
Deploy on AWS/GCP for cloud-based usage
```
👨‍💻 Author

Yash Khot – Cloud & DevOps Enthusiast
