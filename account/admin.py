from django.contrib import admin
from account.models import Account, Wallet, WalletAttribut, WalletBalance, WalletTask

admin.site.register(Account)
admin.site.register(Wallet)
admin.site.register(WalletAttribut)
admin.site.register(WalletBalance)
admin.site.register(WalletTask)
