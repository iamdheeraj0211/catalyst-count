from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.upload_data, name='addorder_url'),
    path('show/', views.showorfileview, name='show_url'),

    path('count/', views.QueryBuildergetAPIView.as_view(), name='count_url'),
    path('query/', views.displayqueryview, name='query_url'),

    
    # path('up/,<int:pk>/', views.updateorderview, name='updateorder_url'),
    # path('dl/<int:pk>/', views.deleteorderview, name='deleteorder_url')
]
