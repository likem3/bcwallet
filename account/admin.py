from utils.admins import BaseAdmin, admin
from account.models import Account, Wallet, WalletAttribut, WalletBalance, WalletTask


class AccountAdmin(BaseAdmin):
    list_display = [
        'uuid',
        'user_id',
        'email',
        'username',
        'status',
    ]
    ordering = ('-created_at',)
    search_fields = ('user_id','email', 'username')


class WalletAdmin(BaseAdmin):
    list_display = [
        'address',
        'user_id',
        'last_balance',
        'balance_change',
        'unit',
        'currency_std',
        'network',
        'time_update',
        'status'
    ]
    ordering = ('-created_at',)
    search_fields = ('address',)

    def last_balance(self, obj):
        return obj.balance.latest('created_at').amount
        
    def balance_change(self, obj):
        return obj.balance.latest('created_at').amount_change

    def unit(self, obj):
        return obj.balance.latest('created_at').unit

    def time_update(self, obj):
        return obj.balance.latest('created_at').created_at

class WalletTaskAdmin(BaseAdmin):
    list_display = [
        'get_wallet_address',
        'get_wallet_user_id',
        'transaction_code',
        'status',
        'attemp',
        'created_at',
        'updated_at',
    ]
    ordering = ('-created_at',)
    search_fields = ('wallet__address', 'wallet__user_id','transaction_code', 'status')

    @admin.display(ordering='wallet__address', description='Address')
    def get_wallet_address(self, obj):
        return obj.wallet.address

    @admin.display(ordering='wallet__user_id', description='UserID')
    def get_wallet_user_id(self, obj):
        return obj.wallet.user_id

admin.site.register(Account, AccountAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletAttribut)
admin.site.register(WalletBalance)
admin.site.register(WalletTask, WalletTaskAdmin)
