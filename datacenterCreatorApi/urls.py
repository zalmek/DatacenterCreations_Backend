from django.contrib import admin
from dcapi import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'api/components/', views.ComponentsApiView.as_view(), name='components-list'),
    path(r'api/components/<int:pk>', views.ComponentsApiView.as_view(), name='components-list'),
    path(r'api/components/<int:pk>/post_to_creation', views.post_component_to_creation, name="add_component_to_creation"),

    path(r'api/creationcomponents/', views.CreationcomponentsApiVIew.as_view(), name='components-list'),
    path(r'api/creationcomponents/<int:pk>', views.CreationcomponentsApiVIew.as_view(), name='components-list'),

    path(r'api/datacentercreations/', views.DatacenterCreationsApiVIew.as_view(), name='components-list'),
    path(r'api/datacentercreations/<int:pk>', views.DatacenterCreationsApiVIew.as_view(), name='components-list'),
    path(r'api/datacentercreations/<int:pk>/user_publish', views.publish_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_approvement', views.approve_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_rejection', views.reject_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_completion', views.complete_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/user_deletion', views.delete_creation, name=''),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]
