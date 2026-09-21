"""
URL configuration for MediScope project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core.views import chatbot


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Chatbot
    path('chatbot/', chatbot, name='chatbot'),

    # Core
    path('', include('core.urls')),

    # Cases
    path('cases/', include('cases.urls')),

    # Quizzes
    path('quizzes/', include('quizzes.urls')),

    # Anatomy
    path('anatomy/', include('anatomy.urls')),

    # AI Checker
    path('ai-checker/', include('ai_checker.urls')),

    # Django authentication
    path('auth/', include('django.contrib.auth.urls')),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'
        ),
        name='logout'
    ),
]


# Serve uploaded media files during local development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )