import stripe
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from core.models import Customer, Job


from .forms import UserModifyForm, CustomerModifyForm, JobCreateStep1

import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

cred = credentials.Certificate(settings.FIREBASE_ADMIN_CONFIG)
firebase_admin.initialize_app(cred)

stripe.api_key = settings.STRIPE_API_SECRET_KEY

@login_required()
def home(request):
    # return render(request, "customer/home.html")
    return redirect(reverse("customer:profile"))

@login_required()
def profile(request):

    user_form = UserModifyForm(instance=request.user)
    customer_form = CustomerModifyForm(instance=request.user.customer)
    password_change_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        action = request.POST.get("action")
        if action == "update_profile":
            user_form = UserModifyForm(request.POST, instance=request.user)
            customer_form = CustomerModifyForm(request.POST, request.FILES,
                                               instance=request.user.customer)

            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()
                messages.add_message(request, messages.SUCCESS, "Your profile has been updated")
                return redirect(reverse("customer:profile"))

        elif action == "change_password":
            password_change_form = PasswordChangeForm(data=request.POST,
                                                      user=request.user)
            if password_change_form.is_valid():
                password_change_form.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Your password has been updated successfully")
                update_session_auth_hash(request, request.user)
                return redirect(reverse("customer:profile"))

            for message in password_change_form.error_messages:
                messages.add_message(request, messages.ERROR, message)

        elif action == "mobile_update":
            idToken = request.POST.get("id_token")
            firebase_user = auth.verify_id_token(idToken)
            request.user.customer.mobile_number = firebase_user["phone_number"]
            request.user.customer.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Mobile number updated successfully")
            return redirect(reverse("customer:profile"))

    return render(request, "customer/profile.html",
                  { "user_form": user_form,
                    "customer_form": customer_form,
                    "password_change_form": password_change_form })

@login_required()
def payment_method(request):
    current_user = request.user
    current_customer = Customer.objects.get(user=current_user)

    if request.method == "POST":
        print("REMOVE")
        # remove card
        stripe.PaymentMethod.detach(
            current_customer.stripe_payment_method_id
        )
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last = ""
        current_customer.save()
        messages.add_message(request, messages.SUCCESS,
                                 "Card Removed Successfully")
        return redirect(reverse("customer:payment_method"))
    
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer["id"]
        current_customer.save()
    
    customer_payment_methods = stripe.Customer.list_payment_methods(
            current_customer.stripe_customer_id,
            type="card",
        )
    
    
    if customer_payment_methods and len(customer_payment_methods) > 0:
        payment_method = customer_payment_methods.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.stripe_card_last = payment_method.card.last4
        current_customer.save()
    
    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last = ""
        current_customer.save()
        
    
    if not current_customer.stripe_payment_method_id:
        print("NO CARD THERE")
        intent = stripe.SetupIntent.create(
            customer = current_customer.stripe_customer_id,
            payment_method_types = ["card"],
        )
    
        return render(request, "customer/payment_method.html", { "client_secret": intent.client_secret, "public_key": settings.STRIPE_API_PUBLIC_KEY})
    else:
        print("CARD THERE")
        return render(request, "customer/payment_method.html")

@login_required()
def create_job(request):
    if not request.user.customer.stripe_customer_id:
        redirect("customer:payment_method")
    customer = Customer.objects.get(user=request.user)
    current_job = Job.objects.filter(customer=customer).last()
    job_create_step1 = JobCreateStep1(instance=current_job)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == 'step1':
            print(request)
            if current_job:
                step1_form = JobCreateStep1(request.POST, request.FILES, instance=current_job)
            else:
                step1_form = JobCreateStep1(request.POST, request.FILES)
            if step1_form.is_valid():
                job = step1_form.save(commit=False)
                job.customer = customer
                job.status = 'pickup'
                job.save()
                print("SUCCES")
                return redirect(reverse("customer:create_job"))
            else:
                print("FAIL")
                job_create_step1=JobCreateStep1(request.POST)
                return render(request, "customer/create_job.html", {
                     "step1_form": job_create_step1
            })
    

    return render(request, "customer/create_job.html", {
        "step1_form": job_create_step1,
        "job": current_job
    })