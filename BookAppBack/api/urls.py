from django.urls import path
from .views import create_custom_user,login_user,validate_token,refresh_token,get_user_details,update_user_details
# from .views import Home
urlpatterns = [
    # path('', Home.as_view()),
    path('register/',create_custom_user,name='create_custom_user'),
    path('login/', login_user, name='login'),
    path('validate-the-token/', validate_token, name='validate-the-token'),
    path('refresh-token/', refresh_token, name='refresh_token'),
    path('details/', get_user_details, name='get_user_details'),
    path('update/', update_user_details, name='update_user_details'),
]
