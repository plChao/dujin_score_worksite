from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connection
from .models import *
from django.db.models import Sum, Count
import logging

logger = logging.getLogger('django')

def index(request):
	filtered_data = all_examinee_info.objects.filter(job='純考生')

	# Check if the filtered data exists
	if filtered_data.exists():
		query_result = filtered_data.aggregate(
			signed_sum=Sum('signed'), 
			all_count=Count('exam_id')
		)
	else:
		query_result = {'signed_sum': 0, 'all_count': 0}

	finish_num=actual_exam_situation.objects.filter(
		exam_id__in=all_examinee_info.objects.filter(job='純考生').values_list('exam_id', flat=True),
		final_score__isnull=False
	).count()

	return render(request, 'index.html', {'s': int(query_result['signed_sum']), 'all': query_result['all_count'], 'f': int(finish_num)})

def table_exists(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
		msg = cursor.fetchall()
		print(msg)
	# messages.success(request, (f"{msg}"))
	return redirect('index')

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
    examinee_info = get_object_or_404(all_examinee_info, exam_id=current_user_id)
    return render(request, 'about.html', {'user_name': examinee_info.name})
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
	teacher_exam_id = request.user.username
	teacher_info = get_object_or_404(all_examinee_info, exam_id=teacher_exam_id)
	exam_qs = exams.objects.filter(exam_id=teacher_info)
	examinee_list = []
	# print(exam_qs)
	for exam in exam_qs:
		examinee_qs = all_examinee_info.objects.filter(
			exam_date=exam.exam_date,
			exam_group=exam.exam_group
		).order_by('exam_date', 'exam_group')
		print(examinee_qs)
		for examinee in examinee_qs:
			actual_score_qs = actual_exam_situation.objects.filter(
				exam_id=examinee.exam_id
			)
			finish_num = actual_score_qs.filter(
				final_examiner__isnull=False
			).count()
			article_num = actual_score_qs.count()
			# examinee_list.append({
			# 	'exam_id': examinee.exam_id,
			# 	'exam_date': examinee.exam_date,
			# 	'exam_group': examinee.exam_group,
			# 	'name': examinee.name,
			# 	'tan_name': examinee.tan_name,
			# 	'finish_num': finish_num,
			# 	'article_num': article_num,
			# })
			examinee_list.append([
				examinee.exam_id,
				examinee.exam_date,
				examinee.exam_group,
				examinee.name,
				examinee.tan_name,
				finish_num,
				article_num,
			])
	return render(request, 'student.html', {'table': examinee_list})

def show_score_table(request, exam_id):
	query_name = f'SELECT name, exam_id from work_cite_all_examinee_info WHERE exam_id = "{exam_id}"'
	query_article = f'select article_id, correctness_minus, fluency_minus, final_score, final_examiner\
		  from work_cite_actual_exam_situation where exam_id = "{exam_id}"\
			order by article_id'
	query_summary = f'select SUM(final_score > 90), SUM(final_score is not null), count(*)\
		  from work_cite_actual_exam_situation where exam_id = "{exam_id}"'
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
		query = f'select work_cite_all_examinee_info.exam_id, work_cite_all_examinee_info.name, count(*) as pass_num\
			from work_cite_all_examinee_info, work_cite_actual_exam_situation \
			WHERE work_cite_all_examinee_info.exam_id = work_cite_actual_exam_situation.exam_id and \
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
		query = f'select work_cite_all_examinee_info.exam_id, work_cite_all_examinee_info.name, count(*) as pass_num\
			from work_cite_all_examinee_info, work_cite_actual_exam_situation \
			WHERE work_cite_all_examinee_info.exam_id = work_cite_actual_exam_situation.exam_id and \
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
			from work_cite_all_examinee_info, work_cite_actual_exam_situation \
			WHERE work_cite_all_examinee_info.exam_id = work_cite_actual_exam_situation.exam_id and \
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
			from work_cite_all_examinee_info, work_cite_actual_exam_situation \
			WHERE work_cite_all_examinee_info.exam_id = work_cite_actual_exam_situation.exam_id and \
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
		query = f'SELECT exam_id from work_cite_all_examinee_info WHERE name like "{name}%"'
		with connection.cursor() as cursor:
			cursor.execute(query)
			results = cursor.fetchall()
		if len(results) == 0:
			return redirect('show_score_table', exam_id=request.POST['searched'])
		exam_id = results[0][0]
	return redirect('show_score_table', exam_id=exam_id)
def update_score_table(request, exam_id):
	current_user_id = request.user.username
	query = f'SELECT name from work_cite_all_examinee_info WHERE exam_id = "{current_user_id}"'
	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchall()
	user_name = results[0][0]

	update_article = {}
	for key, value in request.POST.items():
		print(key, value)
		if value != "" and key != "csrfmiddlewaretoken":
			update_col, article_id = key.rsplit('_', 1)
			query = f'UPDATE work_cite_actual_exam_situation \
						SET {update_col} = {value}, final_examiner = "{user_name}"\
						WHERE exam_id = "{exam_id}" and article_id = "{article_id}";'
			update_article[article_id] = 1
			with connection.cursor() as cursor:
				cursor.execute(query)
	# for key, value in update_article.items():
	# 	final_score = 100 - value 
	# 	query = f'UPDATE work_cite_actual_exam_situation \
	# 				SET final_score = {final_score}\
	# 				WHERE exam_id = "{exam_id}" and article_id = "{key}";'
		with connection.cursor() as cursor:
			cursor.execute(query)
	return redirect('show_score_table', exam_id=exam_id)
def create_user(request):
	df = pd.read_csv('../2024_table/work_cite_all_examinee_info.csv')
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
            from work_cite_awards \
            inner join \
            (select article_id, final_score, exam_id, name from work_cite_actual_exam_situation) as grade \
            on grade.article_id = awards.article_id \
            group by award_id, article_name, exam_id, name) as grade_all\
            inner join \
            (select article_name, award_id, count(*) as qua_num\
            from work_cite_awards\
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