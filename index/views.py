from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import *
from .forms import *
from django.contrib import messages
from user.models import Plan
from django.core.mail import EmailMessage
from django.conf import settings


def myindex(request):
	fds = Team.objects.all()
	qs = Review.objects.all()
	ho = Plan.objects.all()
	ab = About.objects.all()
	context = {'inv':fds,'rev':qs,'plan':ho,'abs':ab}
	return render(request, 'index/index.html',context)


def mycontact(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		name = request.POST.get('name')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		cre = Contact.objects.create(email=email,name=name,subject=subject,message=message)
		msg = EmailMessage('support', cre.email  +  "wants ur  " + cre.message ,
		settings.DEFAULT_FROM_EMAIL,['ewaenpatrick5@gmail.com'],)
		msg.send()
		messages.success(request, 'Thanks for your message we will repyl you shortly')
	return render(request, 'index/contact.html')

