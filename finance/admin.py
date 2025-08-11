from django.contrib import admin
from .models import Transaction, Goal
from import_export import resources
from import_export.admin import ExportMixin

# Register your models here.

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('date', 'title', 'amount', 'transaction_type', 'category')

class TransactionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TransactionResource
    list_display = ('id', 'user', 'date', 'title', 'amount', 'transaction_type', 'category')
    search_fields = ('title',)

# @admin.register(Transaction, TransactionAdmin)
# class TransactionAdminModel(admin.ModelAdmin):
#     list_display = ['id', 'user', 'title', 'amount', 'transaction_type', 'date', 'category']

admin.site.register(Transaction, TransactionAdmin)


@admin.register(Goal)
class TransactionAdminModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'target_amount', 'deadline', 'created_at', 'achieved', 'progress', 'achieved_date']