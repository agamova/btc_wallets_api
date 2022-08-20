from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import Wallet, User, Transaction
from .serializers import WalletSerializer, UserCreateSerializer, TransactionSerializer
from .permissions import IsOwnerOrCreateOnlyPermission


@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrCreateOnlyPermission, )
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'address'

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    @action(methods=['get'], detail=True,
            permission_classes=[IsAuthenticated],
            url_path='transactions', url_name='transactions')
    def transactions(self, request, address):
        user = self.request.user
        wallet = get_object_or_404(Wallet, address=address)
        if wallet.user != user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        wallet_transactions = Transaction.objects.filter(from_wallet=wallet)
        return Response(TransactionSerializer(wallet_transactions, many=True).data)


class TransactionsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = TransactionSerializer

    def get(self, request):
        transactions = Transaction.objects.filter(from_wallet__user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            from_wallet = serializer.validated_data['from_wallet']
            to_wallet = serializer.validated_data['to_wallet']
            amount = serializer.validated_data['amount']
            from_wallet = get_object_or_404(Wallet, address=from_wallet)
            to_wallet = get_object_or_404(Wallet, address=to_wallet)
            if from_wallet.user != request.user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            commission = amount * Decimal('0.015') if from_wallet.user != to_wallet.user else 0
            if amount + commission > from_wallet.balance:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            from_wallet.balance -= (amount + commission)
            to_wallet.balance += amount
            from_wallet.save()
            to_wallet.save()
            transaction = Transaction(
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                commission=commission)
            transaction.save()
            return Response(TransactionSerializer(transaction).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser, ])
def get_statistic(request):
    total_count = Transaction.objects.count()
    profit = Transaction.objects.aggregate(profit=Sum('commission'))['profit']
    return Response(
        {
            'total_transactions': total_count,
            'platform_profit': {'amount': profit, 'currency': "BTC"}
        }
    )
