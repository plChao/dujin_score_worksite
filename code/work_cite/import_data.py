import csv
from datetime import datetime
from .models import *

def import_tan_info(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tan_info_data = tan_info(
                tan_id=row['tan_id'],
                area=row['area'],
                group=row['group'],
                tan_name=row['tan_name']
            )
            tan_info_data.save()
def import_article_info(file_path):
    #  '../2024_table/article_info.csv
    # columns:article_id,article_name
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            article_info_data = article_info(
                article_id=row['article_id'],
                article_name=row['article_name']
            )
            article_info_data.save()

def import_all_examinee_info(file_path):
    # '../2024_table/all_examinee_info.csv
    # columns:name,gender,personal_phone_num,contact_person,
    # contact_person_num,email,tan_id,exam_id,tan_name,job,exam_date,exam_group,signed,finished
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                tan_info.objects.get(tan_id=row['tan_id'])
            except tan_info.DoesNotExist:
                print('tan_info: ' + row['tan_id'] + ' does not exist')
            
            all_examinee_info_data = all_examinee_info(
                exam_id=row['exam_id'],
                name=row['name'],
                gender=row['gender'],
                personal_phone_number=row['personal_phone_number'],
                contact_person=row['contact_person'],
                contact_person_num=row['contact_person_num'],
                email=row['email'],
                tan_id=tan_info.objects.get(tan_id=row['tan_id']),
                tan_name=row['tan_name'],
                job=row['job'],
                exam_date=row['exam_date'],
                exam_group=row['exam_group'],
                signed=row['signed'],
                finished=row['finished']
            )
            all_examinee_info_data.save()
def import_actual_exam_situation(file_path):
    # '../2024_table/actual_exam_situation.csv
    # columns:article_id,name,correctness_minus,fluency_minus,final_score,final_examiner,score_id,exam_id
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                all_examinee_info.objects.get(exam_id=row['exam_id'])
                article_info.objects.get(article_id=row['article_id'])
            except:
                print('all_examinee_info: ' + row['exam_id'] + ' or article_info: ' + row['article_id'] + ' does not exist')
            actual_exam_situation_data = actual_exam_situation(
                exam_id=all_examinee_info.objects.get(exam_id=row['exam_id']),
                article_id=article_info.objects.get(article_id=row['article_id']),
                # correctness_minus=row['correctness_minus'],
                # fluency_minus=row['fluency_minus'],
                # final_score=row['final_score'],
                # final_examiner=row['final_examiner'],
                name=row['name']
            )
            actual_exam_situation_data.save()

def import_exams(file_path):
    # '../../2024_table/exams.csv
    # columns:exam_date,exam_group,exam_id
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            exam_data = exams(
                exam_id=all_examinee_info.objects.get(exam_id=row['exam_id']),
                exam_date=row['exam_date'],
                exam_group=row['exam_group']
            )
            exam_data.save()
def import_awards(file_path):
    # '../../2024_table/awards.csv
    # columns: article_id,award_id,award_name
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                article_info.objects.get(article_id=row['article_id'])
            except article_info.DoesNotExist:
                print('article_info: ' + row['article_id'] + ' does not exist')
            awards_data = awards(
                article_id=article_info.objects.get(article_id=row['article_id']),
                award_id=row['award_id'],
                award_name=row['award_name']
            )
            awards_data.save()

def run():
    import_tan_info('../2024_table/tan_info.csv')
    import_article_info('../2024_table/article_info.csv')
    import_all_examinee_info('../2024_table/all_examinee_info.csv')
    import_actual_exam_situation('../2024_table/actual_exam_situation.csv')
    import_exams('../2024_table/exams.csv')
    import_awards('../2024_table/awards.csv')
