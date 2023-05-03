from django.urls import include, re_path
from Runoff_Visualization import views

urlpatterns = [
    re_path(r'^reg/', views.reg),
    re_path(r'^left_1/', views.left_1),
    re_path(r'^left_2/', views.left_2),
    re_path(r'^right_1/', views.right_1),
    re_path(r'^left_3/', views.left_3),
    re_path(r'^right_3/', views.right_3),
    re_path(r'^weather/', views.weatherAPI.as_view()),
]
