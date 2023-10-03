from django.urls import path
from main import views
urlpatterns = [
    path('',views.index,name='index'),
    path('convert',views.convertview,name='convert'),
    path('download',views.download_excel,name='download')
]
