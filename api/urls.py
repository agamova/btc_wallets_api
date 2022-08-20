from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import WalletViewSet, TransactionsView, create_user, get_statistic


router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallets')

urlpatterns = [
    path('users/', create_user, name='create_user'),
    path('', include(router.urls)),
    path('transactions/', TransactionsView.as_view()),
    path('statistics/', get_statistic, )
]
