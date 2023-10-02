from django.urls import path
from main import views
urlpatterns = [
    path('',views.convertview,name='convert'),
    path('download',views.download_excel,name='download')
]
