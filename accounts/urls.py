from django.urls import path
from .views import signup_api, login_api,user_detail_api, profile_list_api, profile_detail_api,groups_api, invitations_api, open_submissions_api

urlpatterns = [
    path('signup/', signup_api, name='signup_api'),
    path('login/', login_api, name='login_api'),
    path('user/', user_detail_api, name='user_detail_api'),
    path('profiles/', profile_list_api),
    path('profiles/<int:user_id>/', profile_detail_api),
    path('groups', groups_api),
    path('api/open_submissions/', open_submissions_api),
    path('invitations', invitations_api),
    #  path('api/group/', group_detail_api),
]
