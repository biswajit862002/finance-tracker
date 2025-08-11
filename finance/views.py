from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from finance.forms import TransactionForm, GoalForm, ExpenseReportForm
from finance.models import Transaction, Goal
from django.db.models import Sum
from datetime import date, timedelta
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime
from django.utils.dateparse import parse_date
from finance.admin import TransactionResource
from django.contrib import messages
import json
import calendar
from collections import defaultdict


# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'finance/home.html')



# class DashboardView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwergs):
#         user = request.user
#         now = timezone.now().date()
#         today = now
#         yesterday = today - timedelta(days=1)
#         last_7_start = today - timedelta(days=6)   # last 7 days inclusive
#         last_30_start = today - timedelta(days=29) # last 30 days inclusive
#         current_year = today.year

#         transactions = Transaction.objects.filter(user=user)
#         goals = Goal.objects.filter(user=user)

#         # totals
#         total_income = transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#         total_expense = transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
#         net_savings = total_income - total_expense

#         # today / yesterday
#         today_transactions = transactions.filter(date=today)
#         today_income = today_transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#         today_expense = today_transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

#         yesterday_transactions = transactions.filter(date=yesterday)
#         yesterday_income = yesterday_transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#         yesterday_expense = yesterday_transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

#         # Last 7 days (daily)
#         last7_labels = []
#         last7_income = []
#         last7_expense = []
#         for i in range(6, -1, -1):  # 6 days ago ... today
#             d = today - timedelta(days=i)
#             last7_labels.append(d.strftime('%d %b'))  # e.g. "09 Aug"
#             inc = transactions.filter(date=d, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#             exp = transactions.filter(date=d, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
#             last7_income.append(float(inc))
#             last7_expense.append(float(exp))

#         # Last 30 days (daily - 30 points)
#         last30_labels = []
#         last30_income = []
#         last30_expense = []
#         for i in range(29, -1, -1):  # 29 days ago ... today
#             d = today - timedelta(days=i)
#             last30_labels.append(d.strftime('%d %b'))  # you can shorten if needed
#             inc = transactions.filter(date=d, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#             exp = transactions.filter(date=d, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
#             last30_income.append(float(inc))
#             last30_expense.append(float(exp))

#         # Current year (monthly)
#         year_labels = [calendar.month_abbr[m] for m in range(1, 13)]
#         year_income = []
#         year_expense = []
#         for m in range(1, 13):
#             inc = transactions.filter(date__year=current_year, date__month=m, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#             exp = transactions.filter(date__year=current_year, date__month=m, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
#             year_income.append(float(inc))
#             year_expense.append(float(exp))

#         # goal progress (existing logic)
#         remaining_savings = net_savings
#         goal_progress = []

#         today = timezone.now().date()

#         # Sort goals so latest are first (adjust field as needed)
#         goals = goals.order_by('-deadline')

#         # for goal in goals:
#         #     if remaining_savings >= goal.target_amount:
#         #         goal_progress.append({'goal': goal, 'progress': 100})
#         #         remaining_savings -= goal.target_amount
#         #     elif remaining_savings > 0:
#         #         progress = (remaining_savings / float(goal.target_amount)) * 100
#         #         goal_progress.append({'goal': goal, 'progress': progress})
#         #         remaining_savings = 0
#         #     else:
#         #         goal_progress.append({'goal': goal, 'progress': 0})

#         for goal in goals:
#             # Calculate raw progress based on savings
#             if remaining_savings >= goal.target_amount:
#                 progress = 100
#             elif remaining_savings > 0:
#                 progress = (remaining_savings / goal.target_amount) * 100
#             else:
#                 progress = 0

#             # Check achievement condition
#             if today <= goal.deadline and net_savings >= goal.target_amount:
#                 message = "You can achieve your goal"
#                 achieved = True
#                 progress = 100  # Full progress if achieved
#             else:
#                 message = "You cannot achieve your goal"
#                 achieved = False

#             goal_progress.append({
#                 'goal': goal,
#                 'progress': progress,
#                 'achieved': achieved,
#                 'message': message
#             })

#             # Deduct only if within deadline & achieved
#             if achieved:
#                 remaining_savings -= goal.target_amount

#         context = {
#             'transactions': transactions,
#             'goals': goals,
#             'goal_progress': goal_progress[:3],

#             'total_income': total_income,
#             'total_expense': total_expense,
#             'net_savings': net_savings,
            
#             'today_income': today_income,
#             'today_expense': today_expense,
#             'today_savings': today_income - today_expense,

#             'yesterday_income': yesterday_income,
#             'yesterday_expense': yesterday_expense,
#             'yesterday_savings': yesterday_income - yesterday_expense,

#             'last_7_days_income': sum(last7_income),
#             'last_7_days_expense': sum(last7_expense),
#             'last_7_days_savings': sum(last7_income) - sum(last7_expense),

#             'last_30_days_income': sum(last30_income),
#             'last_30_days_expense': sum(last30_expense),
#             'last_30_days_savings': sum(last30_income) - sum(last30_expense),

#             'current_year_income': sum(year_income),
#             'current_year_expense': sum(year_expense),
#             'current_year_savings': sum(year_income) - sum(year_expense),

#             # raw series for charts (JSON strings)
#             'last7_labels_json': json.dumps(last7_labels),
#             'last7_income_json': json.dumps(last7_income),
#             'last7_expense_json': json.dumps(last7_expense),
#             'last30_labels_json': json.dumps(last30_labels),
#             'last30_income_json': json.dumps(last30_income),
#             'last30_expense_json': json.dumps(last30_expense),
#             'year_labels_json': json.dumps(year_labels),
#             'year_income_json': json.dumps(year_income),
#             'year_expense_json': json.dumps(year_expense),
#         }

#         return render(request, 'finance/dashboard.html', context)



class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwergs):
        user = request.user
        
        # Get the current time in your configured timezone (e.g., Asia/Kolkata)
        now = timezone.localtime(timezone.now())
        today = now.date()
        # print('today-----',today)

        yesterday = today - timedelta(days=1)
        # print('yesterday-----',yesterday)

        last_7_start = today - timedelta(days=6)   # last 7 days inclusive
        last_30_start = today - timedelta(days=29) # last 30 days inclusive
        current_year = today.year

        transactions = Transaction.objects.filter(user=user)

        # totals
        total_income = transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = total_income - total_expense

        # today / yesterday
        today_transactions = transactions.filter(date=today)
        today_income = today_transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        today_expense = today_transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

        yesterday_transactions = transactions.filter(date=yesterday)
        yesterday_income = yesterday_transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        yesterday_expense = yesterday_transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

        # Last 7 days (daily)
        last7_labels = []
        last7_income = []
        last7_expense = []
        for i in range(6, -1, -1):  # 6 days ago ... today
            d = today - timedelta(days=i)
            last7_labels.append(d.strftime('%d %b'))  # e.g. "09 Aug"
            inc = transactions.filter(date=d, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
            exp = transactions.filter(date=d, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
            last7_income.append(float(inc))
            last7_expense.append(float(exp))

        # Last 30 days (daily - 30 points)
        last30_labels = []
        last30_income = []
        last30_expense = []
        for i in range(29, -1, -1):  # 29 days ago ... today
            d = today - timedelta(days=i)
            last30_labels.append(d.strftime('%d %b'))  # you can shorten if needed
            inc = transactions.filter(date=d, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
            exp = transactions.filter(date=d, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
            last30_income.append(float(inc))
            last30_expense.append(float(exp))

        # Current year (monthly)
        year_labels = [calendar.month_abbr[m] for m in range(1, 13)]
        year_income = []
        year_expense = []
        for m in range(1, 13):
            inc = transactions.filter(date__year=current_year, date__month=m, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
            exp = transactions.filter(date__year=current_year, date__month=m, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
            year_income.append(float(inc))
            year_expense.append(float(exp))


        # goals part
        achieve_goals = Goal.objects.filter(user=request.user, achieved = True).order_by('-achieved_date', '-deadline')[:3]
        
        # print('goals-----', achieve_goals)

        context = {
            'transactions': transactions,
            'goals': achieve_goals,

            'total_income': total_income,
            'total_expense': total_expense,
            'net_savings': net_savings,
            
            'today_income': today_income,
            'today_expense': today_expense,
            'today_savings': today_income - today_expense,

            'yesterday_income': yesterday_income,
            'yesterday_expense': yesterday_expense,
            'yesterday_savings': yesterday_income - yesterday_expense,

            'last_7_days_income': sum(last7_income),
            'last_7_days_expense': sum(last7_expense),
            'last_7_days_savings': sum(last7_income) - sum(last7_expense),

            'last_30_days_income': sum(last30_income),
            'last_30_days_expense': sum(last30_expense),
            'last_30_days_savings': sum(last30_income) - sum(last30_expense),

            'current_year_income': sum(year_income),
            'current_year_expense': sum(year_expense),
            'current_year_savings': sum(year_income) - sum(year_expense),

            # raw series for charts (JSON strings)
            'last7_labels_json': json.dumps(last7_labels),
            'last7_income_json': json.dumps(last7_income),
            'last7_expense_json': json.dumps(last7_expense),
            'last30_labels_json': json.dumps(last30_labels),
            'last30_income_json': json.dumps(last30_income),
            'last30_expense_json': json.dumps(last30_expense),
            'year_labels_json': json.dumps(year_labels),
            'year_income_json': json.dumps(year_income),
            'year_expense_json': json.dumps(year_expense),
        }

        return render(request, 'finance/dashboard.html', context)

    

class TransactionCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        context = {
            'form' : form,
        }
        return render(request, 'finance/transaction_form.html', context)
    

    def post(self, request, *args, **kwergs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added succssfully!')
            return redirect('dashboard')

        context = {
            'form' : form,
        }
        return render(request, 'finance/transaction_form.html', context)


class TransactionListView(LoginRequiredMixin, View):
    def get_filtered_queryset(self, request):
        filter_option = request.GET.get("filter", "all")
        qs = Transaction.objects.filter(user=request.user)

        today = date.today()
        # print('today-----',today)

        if filter_option == "today":
            qs = qs.filter(date=today)
        elif filter_option == "yesterday":
            qs = qs.filter(date=today - timedelta(days=1))
        elif filter_option == "last_7_days":
            qs = qs.filter(date__gte=today - timedelta(days=7))
        elif filter_option == "last_30_days":
            qs = qs.filter(date__gte=today - timedelta(days=30))
        elif filter_option == "last_6_months":
            qs = qs.filter(date__gte=today - timedelta(days=182))
        elif filter_option == "last_1_year":
            qs = qs.filter(date__gte=today - timedelta(days=365))
        # "all" means no extra filter

        return qs
    
    def get(self, request, *args, **kwargs):
        transactions = self.get_filtered_queryset(request)

        total_income = transactions.filter(transaction_type='Income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(transaction_type='Expense').aggregate(total=Sum('amount'))['total'] or 0

        context = {
            'transactions': transactions,
            'total_income': total_income,
            'total_expense': total_expense,
            'total_savings': total_income - total_expense,
            'selected_filter': request.GET.get("filter", "all")
        }
        return render(request, 'finance/transaction_list.html', context)
    
    

class GoalCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        context = {
            'form' : form,
        }
        return render(request, 'finance/goal_form.html', context)
    

    def post(self, request, *args, **kwergs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created succssfully!')
            return redirect('dashboard')

        context = {
            'form' : form,
        }
        return render(request, 'finance/goal_form.html', context)
    


# class ViewGoalsView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         transactions = Transaction.objects.filter(user=user)
#         goals = Goal.objects.filter(user=user)

#         # Totals
#         total_income = transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
#         total_expense = transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
#         net_savings = total_income - total_expense

#         remaining_savings = net_savings
#         goal_progress = []
#         today = timezone.now().date()

#         # Filtering
#         filter_type = request.GET.get('filter', 'all')
#         search_query = request.GET.get('search', '').strip()
#         deadline_filter = request.GET.get('deadline', '')

#         # Search filter
#         if search_query:
#             goals = goals.filter(name__icontains=search_query)

#         # Deadline filter
#         if deadline_filter:
#             goals = goals.filter(deadline=deadline_filter)

#         # Sort latest first
#         goals = goals.order_by('-deadline')

#         # Filter by type
#         if filter_type == 'latest5':
#             goals = goals[:5]
#         elif filter_type == 'latest10':
#             goals = goals[:10]

#         # Build goal progress data
#         for goal in goals:
#             if remaining_savings >= goal.target_amount:
#                 progress = 100
#             elif remaining_savings > 0:
#                 progress = (remaining_savings / goal.target_amount) * 100
#             else:
#                 progress = 0

#             if today <= goal.deadline and net_savings >= goal.target_amount:
#                 message = "You can achieve your goal"
#                 achieved = True
#                 progress = 100
#             else:
#                 message = "You cannot achieve your goal"
#                 achieved = False

#             goal_progress.append({
#                 'goal': goal,
#                 'progress': progress,
#                 'achieved': achieved,
#                 'message': message
#             })

#             if achieved:
#                 remaining_savings -= goal.target_amount

#         # Achieved/non-achieved filter AFTER progress calculation
#         if filter_type == 'achieved':
#             goal_progress = [g for g in goal_progress if g['achieved']]
#         elif filter_type == 'notachieved':
#             goal_progress = [g for g in goal_progress if not g['achieved']]

#         context = {
#             'goal_progress': goal_progress,
#             'filter_type': filter_type,
#             'search_query': search_query,
#             'deadline_filter': deadline_filter,
#         }
#         return render(request, 'finance/view_goals.html', context)




# class ViewGoalsView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         now = timezone.localtime(timezone.now())
#         today = now.date()

#         print('today-----',today)


#         # Filtering inputs
#         filter_type = request.GET.get('filter', 'all')
#         search_query = request.GET.get('search', '').strip()
#         deadline_filter = request.GET.get('deadline', '')

#         # Base goals queryset
#         goals_qs = Goal.objects.filter(user=user)

#         if search_query:
#             goals_qs = goals_qs.filter(name__icontains=search_query)

#         if deadline_filter:
#             goals_qs = goals_qs.filter(deadline=deadline_filter)

#         # We'll allocate incomes to goals ordered by earliest deadline first
#         goals_qs = goals_qs.order_by('deadline')

#         # Fetch all income transactions for the user, ordered by date (we'll allocate from earliest)
#         incomes_qs = Transaction.objects.filter(user=user, transaction_type='Income').order_by('date')

#         # Build a mutable in-memory list of incomes with a 'remaining' amount to allocate
#         incomes = []
#         for t in incomes_qs:
#             incomes.append({
#                 'id': t.id,
#                 'date': t.date,
#                 'remaining': float(t.amount),
#             })

#         # Helper to allocate amount from incomes within a date window [start, end]
#         def allocate_amount_from_incomes(start, end, amount_needed):
#             """
#             Try to allocate `amount_needed` from incomes list in date order
#             restricted to incomes with start <= date <= end.
#             Returns (allocated_amount, achieved_date) where achieved_date is
#             the date of the income transaction that completed the allocation
#             (or None if not fully satisfied).
#             """
#             allocated = 0.0
#             achieved_date = None
#             remaining_to_allocate = float(amount_needed)

#             for inc in incomes:
#                 if inc['remaining'] <= 0:
#                     continue
#                 if inc['date'] < start or inc['date'] > end:
#                     continue
#                 take = min(inc['remaining'], remaining_to_allocate)
#                 inc['remaining'] -= take
#                 allocated += take
#                 remaining_to_allocate -= take
#                 if remaining_to_allocate <= 1e-9:
#                     # Completed allocation: achieved_date is this income's date
#                     achieved_date = inc['date']
#                     break

#             return allocated, achieved_date

#         # First, reserve amounts for goals already marked achieved in DB so we don't double-use.
#         # If achieved_date exists use that window; otherwise fall back to created_at->deadline.
#         prechecked_goals = list(goals_qs.filter(achieved=True))
#         for g in prechecked_goals:
#             start = g.created_at if hasattr(g, 'created_at') else g.created_at
#             end = g.achieved_date if g.achieved_date else g.deadline
#             # deduct the goal target_amount from incomes in that period
#             try:
#                 amount_to_reserve = float(g.target_amount)
#             except Exception:
#                 amount_to_reserve = 0.0
#             if amount_to_reserve > 0:
#                 allocate_amount_from_incomes(start, end, amount_to_reserve)

#         # Now process goals sequentially (earliest deadline first)
#         goal_progress = []
#         for goal in goals_qs:
#             # If already achieved in DB -> show saved progress (do not recalc)
#             if goal.achieved:
#                 progress = float(goal.progress or 100.0)
#                 achieved = True
#                 message = "You have achieved this goal"
#             else:
#                 # limit incomes used for progress calc to goal.created_at .. min(goal.deadline, today)
#                 window_start = goal.created_at
#                 window_end = min(goal.deadline, today)

#                 # total currently available (remaining) in that period
#                 total_available_now = sum(
#                     inc['remaining'] for inc in incomes
#                     if window_start <= inc['date'] <= window_end
#                 )

#                 target = float(goal.target_amount)

#                 if total_available_now >= target:
#                     # Fully achievable with current available (allocate target and mark achieved)
#                     allocated, achieved_date = allocate_amount_from_incomes(window_start, window_end, target)
#                     progress = 100.0
#                     achieved = True
#                     message = "You have achieved this goal"
#                     # set achieved_date if we computed it (or use today)
#                     goal.achieved = True
#                     goal.achieved_date = achieved_date or today
#                     goal.progress = 100.0
#                     goal.save()
#                 else:
#                     # Not fully achievable yet — record partial allocation (but don't mark achieved)
#                     allocated, _ = allocate_amount_from_incomes(window_start, window_end, total_available_now)
#                     # progress is based on income inside the goal's period only
#                     progress = (allocated / target * 100.0) if target > 0 else 0.0
#                     # If the deadline has passed, lock this progress in DB permanently
#                     if today > goal.deadline:
#                         goal.progress = round(progress, 2)
#                         goal.achieved = False
#                         goal.save()
#                         message = "Goal deadline passed"
#                     else:
#                         # still in-progress
#                         # update stored progress so user can see real-time progress (optional)
#                         goal.progress = round(progress, 2)
#                         goal.save()
#                         message = "You still haven't achieved your goal." if progress < 100.0 else "You have achieved this goal"
#                     achieved = False

#             goal_progress.append({
#                 'goal': goal,
#                 'progress': float(round(progress, 2)),
#                 'achieved': bool(goal.achieved),
#                 'message': message
#             })

#         # Apply post-calculation filters requested by user
#         if filter_type == 'latest5':
#             goal_progress = sorted(goal_progress, key=lambda g: g['goal'].deadline, reverse=True)[:5]
#         elif filter_type == 'latest10':
#             goal_progress = sorted(goal_progress, key=lambda g: g['goal'].deadline, reverse=True)[:10]
#         elif filter_type in ('achieved',):
#             goal_progress = [g for g in goal_progress if g['achieved']]
#         elif filter_type in ('notachieved', 'non_achieved', 'non-achieved'):
#             goal_progress = [g for g in goal_progress if not g['achieved']]

#         context = {
#             'goal_progress': goal_progress,
#             'filter_type': filter_type,
#             'search_query': search_query,
#             'deadline_filter': deadline_filter,
#         }
#         return render(request, 'finance/view_goals.html', context)




class ViewGoalsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        now = timezone.localtime(timezone.now())
        today = now.date()

        # print('today-----',today)


        # Filtering inputs
        filter_type = request.GET.get('filter', 'all')
        search_query = request.GET.get('search', '').strip()
        deadline_filter = request.GET.get('deadline', '')

        # Base goals queryset
        goals_qs = Goal.objects.filter(user=user)

        if search_query:
            goals_qs = goals_qs.filter(name__icontains=search_query)

        if deadline_filter:
            goals_qs = goals_qs.filter(deadline=deadline_filter)

        # We'll allocate incomes to goals ordered by earliest deadline first
        goals_qs = goals_qs.order_by('deadline')

        # Fetch all income transactions for the user, ordered by date (we'll allocate from earliest)
        incomes_qs = Transaction.objects.filter(user=user, transaction_type='Income').order_by('date')

        # Build a mutable in-memory list of incomes with a 'remaining' amount to allocate
        incomes = []
        for t in incomes_qs:
            incomes.append({
                'id': t.id,
                'date': t.date,
                'remaining': float(t.amount),
            })

        # Helper to allocate amount from incomes within a date window [start, end]
        def allocate_amount_from_incomes(start, end, amount_needed):
            """
            Try to allocate `amount_needed` from incomes list in date order
            restricted to incomes with start <= date <= end.
            Returns (allocated_amount, achieved_date) where achieved_date is
            the date of the income transaction that completed the allocation
            (or None if not fully satisfied).
            """
            allocated = 0.0
            achieved_date = None
            remaining_to_allocate = float(amount_needed)

            for inc in incomes:
                if inc['remaining'] <= 0:
                    continue
                if inc['date'] < start or inc['date'] > end:
                    continue
                take = min(inc['remaining'], remaining_to_allocate)
                inc['remaining'] -= take
                allocated += take
                remaining_to_allocate -= take
                if remaining_to_allocate <= 1e-9:
                    # Completed allocation: achieved_date is this income's date
                    achieved_date = inc['date']
                    break

            return allocated, achieved_date

        # First, reserve amounts for goals already marked achieved in DB so we don't double-use.
        # If achieved_date exists use that window; otherwise fall back to created_at->deadline.
        prechecked_goals = list(goals_qs.filter(achieved=True))
        for g in prechecked_goals:
            start = g.created_at if hasattr(g, 'created_at') else g.created_at
            end = g.achieved_date if g.achieved_date else g.deadline
            # deduct the goal target_amount from incomes in that period
            try:
                amount_to_reserve = float(g.target_amount)
            except Exception:
                amount_to_reserve = 0.0
            if amount_to_reserve > 0:
                allocate_amount_from_incomes(start, end, amount_to_reserve)

        # Process goals
        goal_progress = []
        for goal in goals_qs:
            if goal.achieved:
                progress = float(goal.progress or 100.0)
                achieved = True
                message = "You have achieved this goal"

            elif today > goal.deadline:
                # Deadline passed, just use stored value
                progress = float(goal.progress or 0.0)
                achieved = bool(goal.achieved)
                message = "Goal deadline passed"

            else:
                # Active goal
                window_start = goal.created_at
                window_end = min(goal.deadline, today)

                total_available_now = sum(
                    inc['remaining'] for inc in incomes
                    if window_start <= inc['date'] <= window_end
                )
                target = float(goal.target_amount)

                if total_available_now >= target:
                    allocated, achieved_date = allocate_amount_from_incomes(
                        window_start, window_end, target
                    )
                    progress = 100.0
                    achieved = True
                    message = "You have achieved this goal"
                    goal.achieved = True
                    goal.achieved_date = achieved_date or today
                    goal.progress = 100.0
                    goal.save()

                else:
                    allocated, _ = allocate_amount_from_incomes(
                        window_start, window_end, total_available_now
                    )
                    progress = (allocated / target * 100.0) if target > 0 else 0.0
                    achieved = False
                    message = "You still haven't achieved your goal"
                    # Save current progress so it's locked when deadline passes
                    goal.progress = round(progress, 2)
                    goal.save()

            goal_progress.append({
                'goal': goal,
                'progress': float(round(progress, 2)),
                'achieved': bool(goal.achieved),
                'message': message
            })

        # Apply post-calculation filters requested by user
        if filter_type == 'latest5':
            goal_progress = sorted(goal_progress, key=lambda g: g['goal'].deadline, reverse=True)[:5]
        elif filter_type == 'latest10':
            goal_progress = sorted(goal_progress, key=lambda g: g['goal'].deadline, reverse=True)[:10]
        elif filter_type in ('achieved',):
            goal_progress = [g for g in goal_progress if g['achieved']]
        elif filter_type in ('notachieved', 'non_achieved', 'non-achieved'):
            goal_progress = [g for g in goal_progress if not g['achieved']]

        context = {
            'goal_progress': goal_progress,
            'filter_type': filter_type,
            'search_query': search_query,
            'deadline_filter': deadline_filter,
        }
        return render(request, 'finance/view_goals.html', context)


    

class ExpenseReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ExpenseReportForm()
        return render(request, 'finance/expense_report.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ExpenseReportForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            transactions = Transaction.objects.filter(
                user=request.user,
                date__range=[start_date, end_date]
            )

            total_income = sum(t.amount for t in transactions if t.transaction_type == 'Income')
            total_expense = sum(t.amount for t in transactions if t.transaction_type == 'Expense')

            context = {
                'form': form,
                'transactions': transactions,
                'total_income': total_income,
                'total_expense': total_expense,
                'total_savings': total_income - total_expense,
            }

            return render(request, 'finance/expense_report.html', context)

        return render(request, 'finance/expense_report.html', {'form': form})
    

def export_filtered_transactions(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return HttpResponse("Start date and End date are required", status=400)

    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)

    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )

    transactions_resource = TransactionResource()
    dataset = transactions_resource.export(queryset=transactions)
    excel_data = dataset.export('xlsx')

    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"transactions_{start_date}_{end_date}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
    


# def export_transactions(request):
#     user_transactions = Transaction.objects.filter(user = request.user)

#     transactions_resource = TransactionResource()
#     dataset = transactions_resource.export(queryset=user_transactions)

#     excel_data = dataset.export('xlsx')

#     # create an HttpResponse with the correct MIME type for an Excel file
#     response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#     # set the header for downloading the file
#     response['Content-Disposition'] = 'attachment;filename=transactions_report.xlsx'
#     return response
    

def export_transactions(request):
    filter_option = request.GET.get("filter", "all")
    view = TransactionListView()
    filtered_qs = view.get_filtered_queryset(request)

    transactions_resource = TransactionResource()
    dataset = transactions_resource.export(queryset=filtered_qs)

    excel_data = dataset.export('xlsx')

    # create an HttpResponse with the correct MIME type for an Excel file
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # set the header for downloading the file
    response['Content-Disposition'] = f'attachment;filename=transactions_report_{filter_option}.xlsx'
    return response