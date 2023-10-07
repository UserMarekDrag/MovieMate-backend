from django.urls import path
from . import views

urlpatterns = [
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]
