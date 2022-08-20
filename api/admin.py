from django.contrib import admin

from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'balance')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_wallet', 'to_wallet', 'amount')
