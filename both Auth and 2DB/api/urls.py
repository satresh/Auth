from django.urls import path,include
from .views import RegisterView, LoginView, AdminOnlyView, ManagerOnlyView, UserOnlyView,manager, UpdateUserRoleView
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')  # Add basename here


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('AdminOnlyView/', AdminOnlyView.as_view(), name='AdminOnlyView'),
    path('ManagerOnlyView/', ManagerOnlyView.as_view(), name='ManagerOnlyView'),
    path('UserOnlyView/', UserOnlyView.as_view(), name='UserOnlyView'),
    path('manager/', manager.as_view(), name='manager'),
    path('rolechange/', UpdateUserRoleView.as_view(), name='UpdateUserRoleView'),
]
