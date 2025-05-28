# 🎒 Kindergarten Management System

Modern kindergarten management platform for inventory tracking, meal planning, and daily operations.

## ✨ Features

- Kitchen inventory management
- Meal planning and tracking
- Student attendance system
- Staff role management
- Parent notifications
- Daily reports

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Deployment**: Docker

## 🚀 Quick Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd kindergarten-management
```

### 2. Environment Setup
Create `.env` file:

```env
# Basic Configuration
API_V1_STR=/api/v1
BASE_URL=http://localhost:8000
PROJECT_NAME=Kindergarten Manager

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Email (Optional)
EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

```

### 3. Run Application
```bash
docker-compose up --build -d
```

### 4. Setup Database
```bash
docker-compose exec app python -m alembic upgrade head
```

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Main App** | [localhost:8000](http://localhost:8000) | Web interface |
| **API Docs** | [localhost:8000/docs](http://localhost:8000/docs) | Swagger documentation |
| **Admin Panel** | [localhost:8000/admin](http://localhost:8000/admin) | Admin dashboard |


## 🔧 Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Check running containers
docker-compose ps
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Database connection error:**
```bash
docker-compose restart postgres
```

**Permission issues:**
```bash
sudo chown -R $USER:$USER .
```

## 📱 First Time Usage

1. **Login** with default admin credentials
2. **Change password** immediately
3. **Add staff members** and assign roles
4. **Setup kitchen inventory** with ingredients
5. **Create meal plans** for the week
6. **Start daily operations**

## 🛡️ Important Notes

- Change default passwords in production
- Update SECRET_KEY for security
- Setup proper email configuration for notifications
- Regular database backups recommended

---

**Ready to manage your kindergarten efficiently!** 🏫✨