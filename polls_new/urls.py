from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('destination/', views.DestinationView.as_view(), name='destination'),
    path('guide/', views.GuideView.as_view(), name='guide'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('package/', views.PackageView.as_view(), name='package'),
    path('service/', views.ServiceView.as_view(), name='service'),
    path('testimonial/', views.TestimonialView.as_view(), name='testimonial'),
    path('remove/<int:car_id>/', views.remove_from_contact, name='remove_from_contact'),
    path('search/', views.search_results_view, name='search_results'),
    path('add_car/', views.add_car, name='add_car'),
    path('my_cars/', views.my_cars, name='my_cars'),
    path('summ_views/<int:car_id>/', views.summ_views, name='summ_views'),
    path('car/', views.cars, name='car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('add_to_payment/<int:car_id>/', views.add_to_payment, name='add_to_payment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)