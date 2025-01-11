from django.urls import path
from . import views

urlpatterns = [
    path("api/register_user/", views.register_user, name="register_user"),
    path("api/create_blog/", views.create_blog, name="create_blog"),
    path("api/blog_list/", views.blog_list, name="blog_list"),
    path("api/update_blog/<int:pk>/", views.update_blog, name="update_blog"),
    path("api/delete_blog/<int:pk>/", views.delete_blog, name="delete_blog"),
    path("api/update_user_profile/", views.update_user_profile, name="update_user_profile")
]
