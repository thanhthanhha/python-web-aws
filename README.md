# Django Social Media Platform

A full-featured social media web application built with Django, featuring user authentication, profiles, posts, comments, and likes. The application uses AWS S3 for media storage and can be deployed using Docker.

## 🚀 Features

- **User Management**
  - User registration and authentication
  - Profile creation and customization
  - Profile picture upload
  - Bio and job information
  - Password management

- **Social Features**
  - Create, edit, and delete posts
  - Upload images with posts
  - Like posts and comments
  - Nested comment system
  - User search functionality

- **Media Handling**
  - Image upload for posts and profiles
  - Automatic image resizing
  - AWS S3 integration for media storage
  - Public and private media support

## 🛠 Tech Stack

- **Backend**
  - Python 3.11
  - Django
  - Gunicorn
  - PostgreSQL/SQLite3

- **Frontend**
  - Bootstrap 4
  - Crispy Forms
  - Font Awesome

- **Infrastructure**
  - Docker & Docker Compose
  - Nginx
  - AWS S3 for media storage

## 📋 Prerequisites

- Docker and Docker Compose
- AWS Account (for S3 storage)
- Python 3.11 (for local development)

## 🔧 Installation & Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd <project-directory>
```

2. **Environment Variables**
Create a `.env` file in the `python-web-aws` directory with the following variables:
```env
# Database Configuration
EXTERNAL_DB=FALSE  # Set to TRUE for PostgreSQL
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DB_FILE=.

# AWS Configuration (if USE_S3=TRUE)
USE_S3=FALSE
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
```

3. **Build and run with Docker**
```bash
docker-compose up --build
```

4. **Access the application**
Open your browser and navigate to `http://localhost:80`

## 💻 Development Setup

1. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
cd python-web-aws
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Create a superuser**
```bash
python manage.py createsuperuser
```

5. **Run the development server**
```bash
python manage.py runserver
```

## 🏗 Project Structure

```
├── python-web-aws/
│   ├── blog/                 # Blog app
│   │   ├── templates/       # Blog templates
│   │   ├── models.py        # Post, Comment, Like models
│   │   └── views.py         # Blog views
│   ├── users/               # Users app
│   │   ├── templates/       # User templates
│   │   ├── models.py        # Profile model
│   │   └── views.py         # User views
│   ├── pythonweb/           # Main project
│   │   ├── settings.py      # Project settings
│   │   └── urls.py          # Main URL configuration
│   └── manage.py
├── nginx/                    # Nginx configuration
└── docker-compose.yml
```

## 🌟 Features Detailed Explanation

### User System
- Custom user profiles with profile pictures
- Social media bio sections (short and long format)
- Job title display
- Password change functionality
- User search capability

### Post System
- Rich text content
- Image attachment support
- Like system
- Detailed post views
- Edit and delete capabilities
- Post search functionality

### Comment System
- Nested comments (replies)
- Comment likes
- Real-time comment updates

### Media Management
- Automatic image resizing
- S3 storage integration
- Public and private media separation
- Custom storage backends

## 🚀 Deployment

The application is containerized and can be deployed using Docker Compose. The setup includes:

- Web application container (Django + Gunicorn)
- Nginx container for serving static files and reverse proxy
- Optional PostgreSQL database
- AWS S3 integration for media storage

