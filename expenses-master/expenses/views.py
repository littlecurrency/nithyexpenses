import os
import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse


def create_expenses_file(month, year):
    file_name = f"{month:02d}-{year}-expenses.json"
    with open(file_name, "w") as f:
        json.dump({}, f)


def update_expenses_file(date, expense_name, amount):
    month, year = date.month, date.year
    file_name = f"{month:02d}-{year}-expenses.json"

    if not os.path.exists(file_name):
        create_expenses_file(month, year)

    with open(file_name, "r") as f:
        expenses = json.load(f)

    if str(date) not in expenses:
        expenses[str(date)] = []

    expenses[str(date)].append({"expense_name": expense_name, "amount": amount})

    with open(file_name, "w") as f:
        json.dump(expenses, f)


def calculate_daily_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total


def index(request):
    if request.method == "POST":
        expense_name = request.POST.get("expense_name")
        amount = float(request.POST.get("amount"))
        date = datetime.now().date()

        update_expenses_file(date, expense_name, amount)

    json_files = []
    for file in os.listdir():
        if file.endswith("-expenses.json"):
            json_files.append(file)

    month = datetime.now().month
    year = datetime.now().year
    file_nam = f"-{month:02d}-{year}"
    file_name = f"{month:02d}-{year}-expenses.json"

    expenses_data = []
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            expenses = json.load(f)

        for date_str, daily_expenses in expenses.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            daily_total = calculate_daily_total(daily_expenses)
            expenses_data.append({"date": date, "expenses": daily_expenses, "total": daily_total})

    grand_total = 0
    for entry in expenses_data:
        entry_total = sum(expense["amount"] for expense in entry["expenses"])
        entry["total"] = entry_total
        grand_total += entry_total

    return render(request, "expenses/index.html", {
        "expenses_data": expenses_data,
        "file_nam": file_nam,
        "json_files": json_files,
        "grand_total": grand_total,
    })

import csv
from django.http import HttpResponse

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Expense Name', 'Amount'])  # CSV header

    # Get expenses data and write to CSV
    month = datetime.now().month
    year = datetime.now().year
    file_name = f"{month:02d}-{year}-expenses.json"

    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            expenses = json.load(f)

        for date_str, daily_expenses in expenses.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            for expense in daily_expenses:
                writer.writerow([date.date(), expense['expense_name'], expense['amount']])

    return response


from django.http import JsonResponse


def view_expenses(request):
    selected_file = request.GET.get("file")

    expenses = []
    if selected_file:
        with open(selected_file, "r") as f:
            expenses_data = json.load(f)
            for date_str, daily_expenses in expenses_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d")
                for expense in daily_expenses:
                    expenses.append(
                        {"date": date.date(), "expense_name": expense["expense_name"], "amount": expense["amount"]})

    return JsonResponse(expenses, safe=False)
