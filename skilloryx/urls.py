from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('offers/', views.offer_list, name='offers'),
    path('offers/create/', views.offer_create, name='offer_create'),
    path('requests/create/', views.request_create, name='request_create'),
    path('offers/<int:pk>/delete/', views.offer_delete, name='offer_delete'),
    path('offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('propose/<int:offer_id>/', views.propose_swap, name='propose_swap'),
    path('proposals/', views.proposal_list, name='proposals'),
    path('proposals/<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('proposals/<int:pk>/message/', views.proposal_message, name='proposal_message'),
    path('proposals/<int:pk>/accept/', views.proposal_accept, name='proposal_accept'),
    path('proposals/<int:pk>/decline/', views.proposal_decline, name='proposal_decline'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/otp-setup/', views.otp_setup_view, name='otp_setup'),
    path('accounts/otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('video_call/<str:room_name>/', views.video_call, name='video_call'),
    path('about/', views.about_view, name='about'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('contact/', views.contact_view, name='contact'),
]
