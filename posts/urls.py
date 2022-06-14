from django.urls import path
from . import views # class
from .views import * # function

app_name = 'posts'

urlpatterns = [
    path('index/',viewbase, name = 'index'),
    path('view_information/', viewinformation, name='view_information'),  # 추가
    path('view_algorithm/', viewalgorithm, name='view_algorithm'),
    path('view_data/', viewdata, name='view_data'),

    path('view_purchase/', viewpurhase, name='view_purchase'),

    path('view_parser/', viewparser, name='view_parser'),
    path('view_parser/<int:user_id>', cart_algorithm, name='cart_algorithm'),
    path('view_parser2/', viewparser2, name='view_parser2'),
    path('view_parser2/<int:user_id>', cart_algorithm2, name='cart_algorithm2'),
    path('view_parser3/', viewparser3, name='view_parser3'),
    path('view_parser3/<int:user_id>', cart_algorithm3, name='cart_algorithm3'),

    path('view_cart/', cart_view, name='view_cart'),
    path('cart_calculate/', cart_calculate, name='cart_calculate'),

    path('view_cart/delete/<int:id>/', views.delete, name='delete'),

    path('cart_pie/', views.view_piechart, name='cart_pie'),
]