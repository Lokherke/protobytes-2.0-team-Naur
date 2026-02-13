"""
WSGI config for Insurance AI Agent project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_ai_agent.settings')

application = get_wsgi_application()
