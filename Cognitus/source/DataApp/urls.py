from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from DataApp.views import DataViewSet,MainPageView

router = routers.DefaultRouter()

router.register(r'api', DataViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/<int:pk>/', DataViewSet.as_view({'get':'list'}), name='Data_update'),

    path('home',MainPageView.as_view(),name='main_page'),
]
