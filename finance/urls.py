from django.urls import path
from finance.views import HomeView, DashboardView, TransactionCreateView, TransactionListView, GoalCreateView, export_transactions,ViewGoalsView, ExpenseReportView, export_filtered_transactions

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name='dashboard'),
    path("home/", HomeView.as_view(), name='home'),
    # path("", HomeView.as_view(), name='home'),

    path('transaction-add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('transaction-list/', TransactionListView.as_view(), name='transaction_list'),
    path('goal-add/', GoalCreateView.as_view(), name='goal_add'),
    path('generate-report/', export_transactions, name='export_transactions'),
    path('view-goals/', ViewGoalsView.as_view(), name='view_goals'),


    path('expense-report/', ExpenseReportView.as_view(), name='expense_report'),
    path('export-filtered-report/', export_filtered_transactions, name='export_filtered_transactions'),

]