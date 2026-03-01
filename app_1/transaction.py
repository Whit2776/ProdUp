from django.db import transaction
from .models import Wallet, Transaction, Notification
from uuid import uuid4
from datetime import timedelta
from django.utils import timezone

def credit_wallet(receiver, sender, amount ,reference = None):
  success = None
  if reference == None:
    reference = str(uuid4())
  
  receiver = Wallet.objects.select_for_update().get(id=receiver.id)

  before = receiver.balance
  after = before + amount

  receiver.balance = after
  receiver.save()

  Transaction.objects.create(
    wallet=receiver,
    amount=amount,
    transaction_type='credit',
    reference=reference,
    before_balance = before,
    after_balance = after,
  )

  if sender.owner_employee:
    Notification.objects.create(user = receiver.owner_employee, message = f'You have recieved an amount of {receiver.currency}{amount} from {sender.name}')
  success = True

  return {
    'success': success,
    'message': 'Transaction Successful',
    'reference': reference
  }


def debit_wallet(sender, receiver, amount, reference = None):
  res = None
  if reference == None:
    reference = str(uuid4())
  sender = Wallet.objects.select_for_update().get(id=sender.id)
  before = sender.balance
  after = before - amount

  
  recent = Transaction.objects.filter(
    wallet=sender,
    created__gte=timezone.now() - timedelta(seconds=10)
  ).count()

  if amount <= 0:
    return {
    'success': False,
    'message': "Invalid amount",
    'reference': None
  }
  if sender.balance < amount:
    return  {
    'success': False,
    'message': "You do not have enough balance",
    'reference': None
  }
  if sender.daily_spent + amount > sender.daily_limit:
    return  {
    'success': False,
    'message': 'Daily spending Limit has will be exceeded, kindly try again tomorrow',
    'reference': None
  }
  if recent > 3:
    return  {
    'success': False,
    'message': "Too many transfers in a short time",
    'reference': None
  }
  if after  <= sender.minimum_balance:
    return  {
    'success': False,
    'message': "Minimum balance threshold hit, deposit more to make more transactions",
    'reference': None
  }
  
  sender.daily_spent += amount
  sender.balance = after
  sender.save()

  Transaction.objects.create(
    wallet=sender,
    amount=amount,
    transaction_type='debit',
    reference=reference,
    before_balance = before,
    after_balance = after,
  )
  if sender.owner_employee:
    Notification.objects.create(user = sender.owner_employee, message = f'You have transfered an amount of {sender.currency}{amount} to {receiver.name}')
  res = True

  return {
    'success': res,
    'message': "Transaction Successful",
    'reference': reference
  }

def transfer(sender, receiver, amount):
  reference = str(uuid4())
  response = None
  try:
    with transaction.atomic():
      response = debit_wallet(sender, receiver, amount, reference)
      if not response['success']:
        return response
      response = credit_wallet(receiver, sender, amount, reference)
  except Exception as e:
    return {'success': False, 'message':str(e), 'reference': reference}

  return response