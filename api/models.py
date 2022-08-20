from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

from .services import get_address

User = get_user_model()


class Wallet(models.Model):
    address = models.CharField(max_length=34, unique=True, default=get_address, db_index=True)
    balance = models.DecimalField(max_digits=19, decimal_places=8, default=Decimal(1.0), validators=[MinValueValidator(Decimal(0.0))])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')

    def __str__(self):
        return self.address


class Transaction(models.Model):
    from_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions_from')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions_to')
    amount = models.DecimalField(max_digits=19, decimal_places=8)
    commission = models.DecimalField(max_digits=19, decimal_places=8)
