from django.urls import path, include
from rest_framework.authtoken import views as rest
from . import views
from rest_framework import routers
from Accounts import views as profile_views
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register('profile', profile_views.ProfileViewSet)

urlpatterns = [
    # MessageList
    path('message/', views.MessageList.as_view({'get': 'master_list'})),
    path('message/user/<int:pk>', views.MessageList.as_view({'get': 'user_list'})),
    path('message/group/<int:pk>', views.MessageList.as_view({'get': 'group_list'})),
    path('message/user/', views.MessageList.as_view({'post': 'post_user_message'})),
    path('message/group/', views.MessageList.as_view({'post': 'post_group_message'})),
    # MessageDetail
    path('message/<int:pk>', views.MessageDetail.as_view()),
    # UserMessageList
    path('message/user/<int:pk>/user/<int:pk2>', views.UserMessageList.as_view()),
    # GroupMessageList
    path('message/group/<int:pk>/user/<int:pk2>', views.GroupMessageList.as_view()),
    # MessagingGroupList
    path('group/', views.MessagingGroupList.as_view()),
    # MessagingGroupDetail
    path('group/<int:pk>', views.MessagingGroupDetail.as_view()),
    # UserGroupList
    path('user/group/', views.UserGroupList.as_view()),
    # UserGroupDetail
    path('user/<int:pk>/group/<int:pk2>', views.UserGroupDetail.as_view()),
    # UserInboxList
    path('inbox/<int:pk>', views.UserInboxList.as_view()),
    # GroupInboxList
    path('inbox/group/<int:pk>', views.GroupInboxList.as_view()),
    # PollingList
    path('poll/user/<int:pk>/<int:pk2>/<int:last_id>', views.PollingList.as_view({'get': 'poll_user_message'})),
    path('poll/group/<int:pk>/<int:last_id>', views.PollingList.as_view({'get': 'poll_group_message'})),
    path('poll/notification/', views.PollingList.as_view({'get': 'poll_notifications'})),
    # NotificationList
    path('notification/<int:pk>', views.NotificationList.as_view()),
    # HelpUtil
    path('help/', views.HelpUtil.as_view()),
    
    path('', include(router.urls)),
    path('changepassword/', profile_views.ChangePasswordView.as_view(), name='change_password'),
    path('register/', profile_views.RegisterView.as_view(), name='register'),
    path('token/', profile_views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]