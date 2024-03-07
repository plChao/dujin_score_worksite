from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connection

# from .forms import RegisterUserForm

def index(request):
	# 指定考試日期
	query = 'SELECT SUM(signed), count(*) from all_examinee_info where job = "純考生"'
	query_f = f'select count(*) from all_examinee_info \
            JOIN ( \
                SELECT exam_id, SUM(final_score IS NULL) AS unfinish \
                FROM actual_exam_situation GROUP BY exam_id \
            ) AS grade_all \
            ON grade_all.exam_id = all_examinee_info.exam_id \
            WHERE job = "純考生" AND unfinish = 0'
	with connection.cursor() as cursor:
		cursor.execute(query)
		query_result = cursor.fetchall()[0]
		cursor.execute(query_f)
		finish_num = cursor.fetchall()[0][0]

	return render(request, 'index.html', {'s': int(query_result[0]), 'all': query_result[1], 'f': int(finish_num)})

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
def get_article_content(request, article_id):
	import glob
	import os
	print(os.path.abspath(os.path.curdir))
	path = glob.glob(f'./templates/articles/*{article_id}*')
	print(path)
	if len(path) == 0:
		messages.success(request, (f'no articel for ./templates/articles/*{article_id}*'))
		return redirect('index')
	elif len(path) > 1:
		messages.success(request, (f'multiple articel for ./templates/articles/{article_id}*'))
	else:
		return render(request, f'./articles/{article_id}.html', {})
	

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
	print(current_user_id, results)
	return render(request, 'student.html', {'table': results})
def show_score_table(request, exam_id):
	query_name = f'SELECT name, exam_id from all_examinee_info WHERE exam_id = "{exam_id}"'
	query_article = f'select article_id, correctness_minus, fluency_minus, final_score, final_examiner\
		  from actual_exam_situation where exam_id = "{exam_id}"\
			order by article_id'
	query_summary = f'select SUM(final_score > 90), SUM(final_score is not null), count(*)\
		  from actual_exam_situation where exam_id = "{exam_id}"'
	with connection.cursor() as cursor:
		cursor.execute(query_name)
		name_result = cursor.fetchall()
		if len(name_result) == 0:
			messages.success(request, (f'找不到 {exam_id}'))
			return redirect('index')
		cursor.execute(query_article)
		result = cursor.fetchall()
		cursor.execute(query_summary)
		summary = cursor.fetchall()
	
	return render(request, 'score_table.html', {'name': name_result[0][0], 'exam_id': name_result[0][1], 'result': result, 'summary': summary[0]})
def get_award_list(request, award_id):
	if award_id == '1':
		query = f'select all_examinee_info.exam_id, all_examinee_info.name, count(*) as pass_num\
			from all_examinee_info, actual_exam_situation \
			WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
				(tan_id like "T%" or tan_id like "S%") and\
				final_score > 90\
			group by exam_id, name\
			order by pass_num desc'
		awards_name = '個人獎-道親組'
		table_col = ['准考證號碼', '考生名字', '總通過段數']
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
	elif award_id == '2':
		query = f'select all_examinee_info.exam_id, all_examinee_info.name, count(*) as pass_num\
			from all_examinee_info, actual_exam_situation \
			WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
				tan_id like "R%" and\
				final_score > 90\
			group by exam_id, name\
			order by pass_num desc'
		awards_name = '個人獎-道親組'
		table_col = ['准考證號碼', '考生名字', '總通過段數']
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
	elif award_id == '5':
		query = f'select tan_id, tan_name, count(*) as pass_num\
			from all_examinee_info, actual_exam_situation \
			WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
				(tan_id like "T%" or tan_id like "S%") and\
				final_score > 90\
			group by tan_id, tan_name\
			order by pass_num desc'
		awards_name = '團體段數最多-佛堂'
		table_col = ['佛堂編號', '佛堂名稱', '佛堂總通過段數']
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
	elif award_id == '6':
		query = f'select tan_id, tan_name, count(*) as pass_num\
			from all_examinee_info, actual_exam_situation \
			WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
				tan_id like "R%" and\
				final_score > 90\
			group by tan_id, tan_name\
			order by pass_num desc'
		awards_name = '團體段數最多-讀經班'
		table_col = ['讀經班編號', '讀經班名稱', '讀經班總通過段數']
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
	else:
		messages.success(request, ("獎項未計算"))
		return redirect('awards')
	return render(request, 'get_award_list.html', {'awards_name': awards_name,'table_col': table_col, 'result': results})
def search_student(request):
	# print(request.POST)
	if request.POST['searched'] != "" and (request.POST['searched'][0] == '2'):
		exam_id = request.POST['searched']
	else:
		name = request.POST['searched']
		query = f'SELECT exam_id from all_examinee_info WHERE name like "{name}%"'
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
		if len(results) == 0:
			return redirect('show_score_table', exam_id=request.POST['searched'])
		exam_id = results[0][0]
	return redirect('show_score_table', exam_id=exam_id)
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
	df = pd.read_csv('../2024_table/all_examinee_info.csv')
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