from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import connection

# from .forms import RegisterUserForm

def index(request):
    return render(request, 'index.html', {})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.success(request, ("帳號或密碼錯誤，請重試..."))	
			return redirect('login')	

	else:
		return render(request, 'login.html', {})
def about(request):
	current_user_id = request.user.username

	exam_id = f'"{current_user_id}"'
	query = 'SELECT name from all_examinee_info WHERE exam_id = ' + exam_id
	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchall()

	return render(request, 'about.html', {'user_name': results[0][0]})

def logout_user(request):
	logout(request)
	messages.success(request, ("登出成功 !"))
	return redirect('index')