#from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from models import User, Poke
from django.utils import timezone
from datetime import datetime
from django.db.models import Count


def index(request):
	return render(request, 'poke/index.html')

def register(request):
	user = User.objects.filter(email=request.POST.get('email'), password = request.POST.get('password'))
	errors = []
	successes = []
	if len(request.POST.get('u_name')) < 3:
		errors.append('Please enter valid name.')
	if len(request.POST.get('u_alias'))<3:
		errors.append('Please enter valid alias.')
	if not "@" in request.POST.get('email'):
		errors.append('Must enter a valid email.')
	if len(request.POST.get('password'))<8:
		errors.append('Password must be at least 8 characters.')
	if request.POST.get('password') != request.POST.get('cnfm_pswd'):
		errors.append('Passwords do not match.')
	if len(request.POST.get('birth'))<1:
		errors.append('Please enter Date of Birth')
	if len(user) > 0:
		errors.append('This user already exists!')

	if not errors:
		user = User()
		user.name = request.POST.get('u_name')
		user.alias = request.POST.get('u_alias')
		user.email = request.POST.get('email')
		user.password = request.POST.get('password')
		user.confirm = request.POST.get('cnfm_pswd')
		user.dob = request.POST.get('birth')
		user.created_at = timezone.now()
		user.save()
		successes.append('You have successfully registered and may login!')
		print ("Successful Registration")
		return render(request, 'poke/index.html', {'successes': successes})
	else:
		del request.session
		return render(request, 'poke/index.html', {'errors': errors})


def login(request):
	login_errors = []
	user = User.objects.filter(email=request.POST.get('email'), password=request.POST.get('password'))
	if len(user)<1:
		login_errors.append("This user doesn't exist")
		return render(request, 'poke/index.html', {'login_errors': login_errors})
	else:
		request.session['user_id'] = user[0].id
		return redirect('/dashboard')

def dashboard(request):
	if "user_id" in request.session:
		users = User.objects.all().exclude(id=request.session['user_id'])
		pokes = Poke.objects.all()
		user_poke_count = Poke.objects.all().filter(poked=request.session['user_id'])
		all_users = Poke.objects.filter(poked=request.session['user_id']).exclude(id=request.session['user_id'])
		user = User.objects.get(id=request.session['user_id'])
		context = {
			'users': users, 
			'pokes': pokes, 
			'user_poke_count': user_poke_count, 
			'all_users': all_users,
			'user': user
		}
		return render(request, 'poke/dashboard.html', context)
	else:
		del request.session
		return redirect('/')

def poke(request, user_id):
	#print('I was here inside poke')

	poker = User.objects.get(id=request.session['user_id'])
	poked = User.objects.get(id=user_id)
	#print (poked.name)
	poke = Poke()
	poke.poker = poker
	poke.poked = poked
	poke.created_at = timezone.now()
	poke.counter+=1
	poke.save()
	return redirect('/dashboard')

def logout(request):
	print ("Logging Out")
	del request.session['user_id']
	return redirect('/')