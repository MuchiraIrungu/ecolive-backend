from django.urls import path
from . import views

urlpatterns = [
    path('available/', views.AvailableHivesView.as_view(), name='available'),
    path('<int:pk>/invest/', views.InvestInHiveView.as_view(), name='invest'),
    path('portfolio/', views.MyPortfolioView.as_view(), name='portfolio'),
    path('farmer/hives/', views.FarmerHivesView.as_view(), name='farmer-hives'),
    path('farmer/hives/<int:hive_pk>/update/', views.SubmitUpdateView.as_view(), name='submit-update'),
]