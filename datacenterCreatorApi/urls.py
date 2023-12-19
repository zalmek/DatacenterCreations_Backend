from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from dcapi import views
from django.urls import include, path
from rest_framework import routers, permissions

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router.register(r'api/user', views.UserViewSet, basename='user')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),

    path('', include(router.urls)),
    path(r'api/components/', views.ComponentsApiView.as_view(), name='components-list'),
    path(r'api/components/<int:pk>', views.ComponentsApiView.as_view(), name='components-list'),
    path(r'api/components/<int:pk>/post_to_creation', views.post_component_to_creation,
         name="add_component_to_creation"),

    path(r'api/creationcomponents/', views.CreationcomponentsApiVIew.as_view(), name='components-list'),
    path(r'api/creationcomponents/<int:pk>', views.CreationcomponentsApiVIew.as_view(), name='components-list'),

    path(r'api/datacentercreations/', views.DatacenterCreationsApiVIew.as_view(), name='components-list'),
    path(r'api/datacentercreations/<int:pk>', views.DatacenterCreationsApiVIew.as_view(), name='components-list'),
    path(r'api/datacentercreations/<int:pk>/user_publish', views.publish_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_approvement', views.approve_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_rejection', views.reject_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_completion', views.complete_creation, name=''),
    path(r'api/datacentercreations/<int:pk>/moderator_deletion', views.delete_creation, name=''),

    path('admin/', admin.site.urls),
]
