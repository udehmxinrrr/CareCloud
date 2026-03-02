from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import requests
from requests.auth import HTTPBasicAuth
from careapp.models import Appointment
import json
from careapp.credentials import MpesaAccessToken, LipanaMpesaPpassword


# Create your views here.
def home(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def appointments(request):
    if request.method == 'POST':
        all = Appointment(
            Name = request.POST['name'],
            email = request.POST['email'],
            Phone = request.POST['phone'],
            datetime = request.POST['date'],
            Department = request.POST['department'],
            Doctor = request.POST['doctor'],
            Message = request.POST['message'],

        )
        all.save()
        return render(request, 'appointments.html')

    else:
        return render(request, 'appointments.html')



def about(request):
    return render(request, 'about.html')

def show(request):
    allappointments = Appointment.objects.all()
    return render(request, 'show.html', {'allappointments': allappointments})

def delete(request, id):
    appoint = Appointment.objects.get(id=id)
    appoint.delete()
    return redirect('/show')


def edit(request, id):
    editappointment = get_object_or_404 (Appointment, id=id)

    if request.method == 'POST':
        editappointment.Name = request.POST['name']
        editappointment.email = request.POST['email']
        editappointment.Phone = request.POST['phone']
        editappointment.datetime = request.POST['date']
        editappointment.Department = request.POST['department']
        editappointment.Doctor = request.POST['doctor']
        editappointment.Message = request.POST['message']
        editappointment.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html', {'editappointment': editappointment})







#Mpesa Views
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    return render(request, 'pay.html')


def payment_result(request):
    return render(request, 'payment_result.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/mpesa/callback",  # Update with your actual callback URL
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")

        if result_code == "0":
            # STK push was sent successfully, but payment not yet confirmed
            # Save as Pending - will be updated by callback
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Pending"  # Changed from "Success" to "Pending"
            )
            transaction.save()

            context = {
                'success': True,
                'transaction_id': transaction_id,
                'amount': amount,
                'phone': phone
            }
            return render(request, 'payment_result.html', context)
        else:
            error_message = response_data.get("ResponseDescription", "Transaction failed")
            context = {
                'success': False,
                'error_message': error_message,
                'result_code': result_code,
                'amount': amount,
                'phone': phone
            }
            return render(request, 'payment_result.html', context)

    return HttpResponse("Invalid Request method")


# Add this new callback function to handle M-Pesa callback
def mpesa_callback(request):
    """
    Handles M-Pesa callback to update transaction status
    """
    if request.method == "POST":
        try:
            import json
            callback_data = json.loads(request.body)

            # Extract callback data
            result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')

            # Find the transaction
            try:
                transaction = Transaction.objects.get(transaction_id=checkout_request_id)

                if result_code == 0:
                    # Payment successful
                    transaction.status = "Success"

                    # Extract M-Pesa receipt number if available
                    callback_metadata = callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata',
                                                                                                 {}).get('Item', [])
                    for item in callback_metadata:
                        if item.get('Name') == 'MpesaReceiptNumber':
                            transaction.mpesa_receipt = item.get('Value')
                            break
                else:
                    # Payment failed or cancelled
                    transaction.status = "Failed"

                transaction.save()

            except Transaction.DoesNotExist:
                pass

        except Exception as e:
            print(f"Callback error: {str(e)}")

    # Always return success response to M-Pesa
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})


def transactions_list(request):
    # Only show successfully completed transactions
    transactions = Transaction.objects.filter(status="Success").order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})
