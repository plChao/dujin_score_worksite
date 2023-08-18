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
def student(request):
	current_user_id = request.user.username

	query = f'select info.exam_id, exam_date, exam_group, name, tan_name, finish_num, article_num\
		  from (SELECT examinee.exam_id, examinee.exam_date, examinee.exam_group, name, tan_name\
    FROM all_examinee_info AS examinee \
    JOIN (SELECT exam_date, exam_group FROM exams WHERE exam_id = "{current_user_id}")AS exam_group_table \
    ON examinee.exam_date = exam_group_table.exam_date \
    and examinee.exam_group = exam_group_table.exam_group) as info \
    JOIN (SELECT exam_id, SUM(final_examiner is not null) AS finish_num, count(article_id) AS article_num \
                FROM actual_exam_situation \
                GROUP BY exam_id) as number on info.exam_id = number.exam_id \
    order by exam_date'
	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchall()
	return render(request, 'student.html', {'table': results})
def show_score_table(request, exam_id):
	query_name = f'SELECT name from all_examinee_info WHERE exam_id = "{exam_id}"'
	query_article = f'select article_id, correctness_minus, fluency_minus, final_score, final_examiner\
		  from actual_exam_situation where exam_id = "{exam_id}"\
			order by article_id'
	with connection.cursor() as cursor:
		cursor.execute(query_name)
		name = cursor.fetchall()[0][0]
		cursor.execute(query_article)
		result = cursor.fetchall()
	
	return render(request, 'score_table.html', {'name': name, 'exam_id': exam_id, 'result': result})
def search_student(request):
	print(request.POST)
	return redirect('show_score_table', exam_id=request.POST['searched'])
def update_score_table(request, exam_id):
	current_user_id = request.user.username
	query = f'SELECT name from all_examinee_info WHERE exam_id = "{current_user_id}"'
	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchall()
	user_name = results[0][0]

	update_article = {}
	for key, value in request.POST.items():
		print(key, value)
		if value != "" and key != "csrfmiddlewaretoken":
			update_col, article_id = key.rsplit('_', 1)
			query = f'UPDATE actual_exam_situation \
						SET {update_col} = {value}, final_examiner = "{user_name}"\
						WHERE exam_id = "{exam_id}" and article_id = "{article_id}";'
			update_article[article_id] = 1
			with connection.cursor() as cursor:
				cursor.execute(query)
	# for key, value in update_article.items():
	# 	final_score = 100 - value 
	# 	query = f'UPDATE actual_exam_situation \
	# 				SET final_score = {final_score}\
	# 				WHERE exam_id = "{exam_id}" and article_id = "{key}";'
		with connection.cursor() as cursor:
			cursor.execute(query)
	return redirect('show_score_table', exam_id=exam_id)


def logout_user(request):
	logout(request)
	messages.success(request, ("登出成功 !"))
	return redirect('index')