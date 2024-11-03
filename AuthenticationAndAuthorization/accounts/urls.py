from django.urls import path
from .views import RegisterView, LoginView, AdminOnlyView, ManagerOnlyView, UserOnlyView,manager, UpdateUserRoleView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('AdminOnlyView/', AdminOnlyView.as_view(), name='AdminOnlyView'),
    path('ManagerOnlyView/', ManagerOnlyView.as_view(), name='ManagerOnlyView'),
    path('UserOnlyView/', UserOnlyView.as_view(), name='UserOnlyView'),
    path('manager/', manager.as_view(), name='manager'),
    path('rolechange/', UpdateUserRoleView.as_view(), name='UpdateUserRoleView'),
]
