



from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verification/', views.verify, name='verification'),
    # path('certificate/<int:certificate_id>/', views.show_certificate, name='show_certificate'),
    # path('certificate/<int:certificate_id>/download/', views.download_certificate, name='download_certificate'),
     path('certificate/generate/', views.generate_certificate_pdf, name='generate_certificate_pdf'),
    path('certificate/display/<int:certificate_id>/', views.certificate_display, name='certificate_display'),
    path('certificate/download/<int:certificate_id>/', views.download_certificate_pdf, name='download_certificate_pdf'),
    # Add other URL patterns as needed
]
