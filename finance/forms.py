from django import forms
from finance.models import Transaction, Goal


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'date', 'category']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'deadline']



class ExpenseReportForm(forms.Form):
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

