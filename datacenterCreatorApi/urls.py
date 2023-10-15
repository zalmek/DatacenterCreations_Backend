from django.contrib import admin
from dcapi import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'components/', views.get_components, name='components-list'),
    path(r'components/post/', views.post_component, name='components-post'),
    path(r'components/<int:pk>/', views.get_component, name='components-detail'),
    path(r'components/<int:pk>/put/', views.put_component, name='components-put'),
    path(r'components/<int:pk>/delete/', views.delete_component, name='components-delete'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]