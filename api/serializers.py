import re
from django.core.cache import cache
from rest_framework import serializers
from decimal import Decimal
from .models import Wallet
from .services import get_decimal_rate


TRANSACTION_ERR_MSG = "Transaction amount can't be zero or less"
USERNAME_ERR_MSG = (
            "Enter a valid username. This value may contain only English letters, "
            "numbers, and @/./+/-/_ characters."
        )
ADDRESS_ERR_MSG = "Invalid operation. Make sure the addresses do not match."
USERNAME_REGEX = r"^[\w.@+-]+\Z"


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('address', 'balance')
        read_only_fields = ('address',)

    def get_balance(self, obj):
        rate = cache.get("rate")
        rate = get_decimal_rate(rate)
        return [
            {'amount': obj.balance, 'currency': 'BTC'},
            {'amount': obj.balance / rate, 'currency': 'USD'}
        ]

    def validate(self, data):
        user = self.context['request'].user
        if user.wallets.count() >= 10:
            raise serializers.ValidationError('Wallets limit exceeded')
        return data


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate_username(self, value):
        if not re.match(USERNAME_REGEX, value):
            raise serializers.ValidationError(USERNAME_ERR_MSG)
        return value


class TransactionSerializer(serializers.Serializer):
    from_wallet = serializers.CharField()
    to_wallet = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=8)
    commission = serializers.DecimalField(max_digits=19, decimal_places=8, read_only=True)

    def validate(self, data):
        if data['from_wallet'] == data['to_wallet']:
            raise serializers.ValidationError(ADDRESS_ERR_MSG)
        if data['amount'] <= Decimal(0):
            raise serializers.ValidationError(TRANSACTION_ERR_MSG)
        return data
