from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .models import Wallet, User, Transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import TransactionSerializer
from rest_framework.decorators import api_view
import datetime

def home(request):
    return render(request, 'pay/index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return render(request, 'pay/index.html')
        else:
            messages.error(request, "Invalid Credentials !!! Try again.")
            return render(request, 'pay/login.html')
        
    return render(request, 'pay/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            u = User.objects.create(username = username)
        except IntegrityError:
            messages.error(request, "Username already taken")
            return render(request, 'pay/register.html')
        u.set_password(password)
        u.save()
        w = Wallet.objects.create(username = username, owner=u)
        w.save()
        messages.success(request,"User created successfully !")
        return render(request, 'pay/login.html')

    return render(request, 'pay/register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

@login_required
def add_money(request):
    if request.method == "POST":
        amount = float(request.POST['amount'])
        if amount>0:
            instance = Wallet.objects.get(owner = request.user)
            instance.balance += amount
            instance.money_added += amount
            instance.save()
            Transaction.objects.create(wallet = instance, text = "Added", amount = amount)
            messages.success(request, "Money added successfully")
            return render(request, 'pay/add_money.html', {'balance':instance.balance})
        else:
            messages.error(request, 'Amount should be greater than zero.')
            return render(request, 'pay/add_money.html', )
    return render(request, 'pay/add_money.html')

@login_required
def pay_money(request):
    if request.method == "POST":
        sender = Wallet.objects.get(owner = request.user)
        receiver_username = request.POST['username']
        try:
            receiver = Wallet.objects.get(username = receiver_username)
        except Wallet.DoesNotExist:
            messages.error(request, "Invalid Username")
            return render(request, 'pay/pay_money.html',)
        amount = float(request.POST['amount'])
        if amount <= sender.balance and amount > 0:
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()
            Transaction.objects.create(wallet = sender, text = "Paid", amount = amount)
            Transaction.objects.create(wallet = receiver, text = "Received", amount = amount)
            messages.success(request, "Money Sent Successfully !")
            return render(request, 'pay/pay_money.html', {'balance': sender.balance})
            
        else:
            messages.error(request, "Invalid Amount / Insufficient funds !")
            return render(request, 'pay/pay_money.html',)
        
    return render(request, 'pay/pay_money.html', )

@login_required
def current_balance(request):
    instance = Wallet.objects.get(owner = request.user)
    balance = instance.balance
    return render(request, 'pay/balance.html', {'balance' : balance})

@login_required
def transaction_log(request):
    wallet = Wallet.objects.get(owner = request.user)
    try:
        queries = Transaction.objects.filter(wallet = wallet)
    except Transaction.DoesNotExist:
        messages.error(request, "No transactions")
        return render(request, 'pay/index.html')
    return render(request, 'pay/transaction.html', {'queries': queries})

# class TransactionViewset(viewsets.ModelViewSet):
    
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

@api_view(['GET'])
def transact_add_view(request, wallet_id):
    wallet = Wallet.objects.get(wallet_id = wallet_id)
    transactions = Transaction.objects.filter(wallet = wallet)
    amount_added = 0
    for x in transactions:
        if x.created_at.month == datetime.datetime.now().month and x.text == "Added":
            amount_added += x.amount 
    amount = {'amount_added' : amount_added}
    # serializer = TransactionSerializer(data=transactions, many=True)
    # if serializer.is_valid():
        # serializer.save()
    return Response(amount)

@api_view(['GET'])
def transact_paid_view(request, wallet_id):
    wallet = Wallet.objects.get(wallet_id = wallet_id)
    transactions = Transaction.objects.filter(wallet = wallet)
    amount_paid = 0
    for x in transactions:
        if x.created_at.month == datetime.datetime.now().month and x.text == "Paid":
            amount_paid += x.amount 
    amount = {'amount_paid' : amount_paid}
    # serializer = TransactionSerializer(data=transactions, many=True)
    # if serializer.is_valid():
        # serializer.save()
    return Response(amount)