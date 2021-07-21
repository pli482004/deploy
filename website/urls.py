from django.urls import path

from website import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/about', views.about, name='about'),
    path('/select', views.select, name='select'),
    path('/register', views.register, name='register'),
    path("/login", views.login_view, name="login"),
    path("/logout", views.logout_view, name="logout"),
    path("/draw", views.draw, name="draw"),
    path("/bookmark", views.bookmark, name="bookmark")
]