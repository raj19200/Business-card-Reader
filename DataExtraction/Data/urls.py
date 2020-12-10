from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('demo',views.demo,name="demo"),
    path('show',views.show,name="show"),
    path('<int:id>/update',views.update,name="update"),
    path('detail',views.detail,name="detail"),
    path('<int:id>/',views.edittemp,name="editdata"),
    path('',views.index,name="index"),
    path('search',views.search,name="search"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)