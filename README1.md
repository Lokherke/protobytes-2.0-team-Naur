# Insurance AI Agent

An AI-powered assistant designed to simplify and bring transparency to the insurance claim process in Nepal.

## Features

- **AI Damage Detection**: Identifies visible damage from uploaded images
- **Policy Clause Mapping**: Links detected damage to relevant insurance policy sections
- **Claim Eligibility Check**: Instantly informs users whether damage is likely covered
- **AI Chat Assistant**: Answers user questions in simple language about claims, coverage, and rejections
- **Transparency Insights**: Explains common claim rejection tactics and how users can avoid them

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd insurance_ai_agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
insurance_ai_agent/
├── insurance_ai_agent/     # Main Django project
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI configuration
├── core/                    # Core app (home, about, policies)
│   ├── models.py            # InsurancePolicy, PolicyClause models
│   ├── views.py             # Core views
│   └── urls.py              # Core URL patterns
├── claims/                  # Claims app (damage analysis, claims)
│   ├── models.py            # DamageClaim, DamageType models
│   ├── views.py             # API endpoints for claims
│   └── urls.py              # Claims URL patterns
├── chat/                    # Chat app (AI assistant)
│   ├── models.py            # ChatSession, ChatMessage models
│   ├── views.py             # Chat API endpoints
│   └── urls.py              # Chat URL patterns
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       └── main.js          # Main JavaScript file
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── core/
│       └── home.html        # Home page template
├── media/                   # User-uploaded files
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## API Endpoints

### Claims API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/claims/analyze/` | POST | Analyze damage image |
| `/api/claims/submit/` | POST | Submit a new claim |
| `/api/claims/status/<id>/` | GET | Get claim status |
| `/api/claims/damage-types/` | GET | Get all damage types |
| `/api/claims/rejection-reasons/` | GET | Get common rejection reasons |

### Chat API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat/message/` | POST | Send chat message |
| `/api/chat/history/<session_id>/` | GET | Get chat history |
| `/api/chat/clear/` | POST | Clear chat history |

### Core API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/policies/` | GET | Get all insurance policies |

## Usage

### For Users

1. **Analyze Damage**: Upload a photo of vehicle damage to get AI analysis
2. **Check Eligibility**: See if your damage is likely covered by insurance
3. **View Policy Clauses**: Understand which policy sections apply to your damage
4. **Get Repair Estimate**: See estimated repair costs
5. **Chat with AI**: Ask questions about insurance claims in simple language
6. **Learn About Rejections**: Understand common rejection reasons and how to avoid them

### For Administrators

1. **Access Admin Panel**: Go to `/admin/` and log in
2. **Manage Policies**: Add/edit insurance policies and their clauses
3. **View Claims**: See all submitted claims and their status
4. **Manage Damage Types**: Add/edit predefined damage types

## Customization

### Adding Real AI Model

The current implementation uses simulated AI analysis. To integrate a real ML model:

1. Update the `analyze_damage` view in `claims/views.py`
2. Replace the simulated detection with actual model inference:

```python
# Example integration with TensorFlow/PyTorch model
from .ml_model import DamageDetectionModel

model = DamageDetectionModel()

def analyze_damage(request):
    image = request.FILES.get('image')
    # Run actual model inference
    results = model.predict(image)
    return JsonResponse(results)
```

### Changing Database

To use PostgreSQL instead of SQLite:

1. Install psycopg2: `pip install psycopg2`
2. Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure allowed hosts: `ALLOWED_HOSTS = ['yourdomain.com']`
- [ ] Use HTTPS
- [ ] Set up proper static files serving (Whitenoise or CDN)
- [ ] Configure media files storage (AWS S3 or similar)
- [ ] Set up database backups

### Deployment Options

1. **PythonAnywhere** (Free tier available)
2. **Heroku** (Free tier available)
3. **DigitalOcean** / **AWS** / **GCP**
4. **VPS** with Nginx + Gunicorn

### Using Gunicorn + Nginx

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn insurance_ai_agent.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support, email support@insuranceai.np or create an issue in the repository.

## Acknowledgments

- Developed for the insurance industry in Nepal
- Designed to promote transparency and empower policyholders
- Built with Django and modern web technologies