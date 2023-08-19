from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connection
import pandas as pd

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
def create_user(request):
	df = pd.read_csv('../2023_table/all_examinee_info.csv')
	df = df[df['job'] == '評鑑老師']
	account_df = pd.DataFrame()
	for index, row in df.iterrows():
		new_row = pd.DataFrame([{'username': row['exam_id'], 'password': 'a0' + str(row['personal_phone_num']), 'name': row['name']}])
		print(new_row)
		try:
			new_user = User.objects.create_user(row['exam_id'], "", 'a0' + row['personal_phone_num'], last_name=row['name'])
		except:
			pass
		account_df = pd.concat([account_df, new_row], ignore_index=True)
		# myuser = User.objects.create_user('username', 'example@gmail.com', 'youPassword')
	messages.success(request, ("建立使用者完畢 !"))
	account_df.to_csv('create_account.csv', index=False)
	return redirect('index')

def awards(request, exam_id="", awards_id=""):
	if exam_id == "" and awards_id == "":
		query = f'select award_qualify.article_name, exam_id, grade_all.name, pass_num, cho, qua_num, (pass_num = award_qualify.qua_num) as pass\
            from (select article_name, award_id, exam_id, name, SUM(final_score is not null and final_score > 90) as pass_num, COUNT(*) as cho \
            from awards \
            inner join \
            (select article_id, final_score, exam_id, name from actual_exam_situation) as grade \
            on grade.article_id = awards.article_id \
            group by award_id, article_name, exam_id, name) as grade_all\
            inner join \
            (select article_name, award_id, count(*) as qua_num\
            from awards\
            group by award_id, article_name) as award_qualify \
            on award_qualify.award_id = grade_all.award_id \
            where award_qualify.qua_num = grade_all.cho and pass_num = award_qualify.qua_num\
            order by award_qualify.award_id, exam_id;'
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
		return render(request, 'awards.html', {'table': results})

def logout_user(request):
	logout(request)
	messages.success(request, ("登出成功 !"))
	return redirect('index')