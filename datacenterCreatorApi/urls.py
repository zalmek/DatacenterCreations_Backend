from django.contrib import admin
from dcapi import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'components/', views.ComponentsApiView.as_view(), name='components-list'),
    path(r'components/<int:pk>', views.ComponentsApiView.as_view(), name='components-list'),

    path(r'creationcomponents/', views.CreationcomponentsApiVIew.as_view(), name='components-list'),
    path(r'creationcomponents/<int:pk>', views.CreationcomponentsApiVIew.as_view(), name='components-list'),

    path(r'datacentercreations/', views.DatacenterCreationsApiVIew.as_view(), name='components-list'),
    path(r'datacentercreations/<int:pk>', views.DatacenterCreationsApiVIew.as_view(), name='components-list'),
    path(r'datacentercreations/user_publish', views.publish_creation, name=''),
    path(r'datacentercreations/moderator_approvement', views.approve_creation, name=''),
    path(r'datacentercreations/moderator_rejection', views.reject_creation, name=''),
    path(r'datacentercreations/moderator_completion', views.complete_creation, name=''),
    path(r'datacentercreations/moderator_deletion', views.delete_creation, name=''),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]
