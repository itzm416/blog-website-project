from django.urls import path
from blogapp import views

urlpatterns = [
    path('', views.home, name='home'),

    # profile
    path('profile/', views.profile, name='p'),
    path('about/', views.about, name='about'),
    path('update-user-details/', views.user_update, name='u'),
    path('update-profile-picture-bio/', views.user_image_bio, name='image'),
    path('delete/', views.user_delete, name='delete'),

    # blog
    path('blog/', views.blog, name='blog'),

    # read blog
    path('read-blog/<slug:slug>/', views.read_post, name='read'),
    path('comment/<slug:slug>/', views.comment, name='comment'),
    path('deletecomment/<slug:slug>/', views.delete_comment, name='deletecomment'),
    path('subdeletecomment/<slug:slug>/', views.delete_sub_comment, name='subdeletecomment'),
    path('subcomment/<slug:slug>/', views.subcomment, name='subcomment'),

    # dashboard read blog
    path('d-dashboard-blog-read/<slug:slug>/', views.dashboard_blog_read, name='dashboardblogread'),
    path('d-comment/<slug:slug>/', views.d_comment, name='d_comment'),
    path('d-deletecomment/<slug:slug>/', views.d_delete_comment, name='d_deletecomment'),
    path('d-subdeletecomment/<slug:slug>/', views.d_delete_sub_comment, name='d_subdeletecomment'),
    path('d-subcomment/<slug:slug>/', views.d_subcomment, name='d_subcomment'),

    path('latest-blog/', views.latest_blog, name='latestblog'),
    path('addblog/', views.add_blog, name='addpost'),
    path('updateblog/<slug:slug>/', views.update_blog, name='updatepost'),
    path('dashboard/', views.user_dashboard, name='dashboard'),

    path('blog-category/<slug:slug>/', views.blog_category, name='blogcategory'),
    path('search-blog/', views.search_blog, name='searchblog'),
    path('author-profile/<slug:author>/', views.author_profile, name='authorprofile'),
    path('deleteblog/<slug:slug>/',views.delete_blog, name='deletepost'),

    # login logout
    path('login/', views.user_login, name='l'),
    path('logout/', views.user_logout, name='logout'),

    # sigup
    path('signup/', views.user_signup, name='s'),
    path('account-verify/<slug:token>', views.user_account_verify, name='account-verify'),

    # password change
    path('password-change/', views.password_change, name='c'),
    
    # password reset
    path('password-reset/<slug:token>', views.user_password_reset, name='reset-password'),
    path('user-email-send/', views.user_email_send, name='send-email')
]

