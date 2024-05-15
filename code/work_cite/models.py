from django.db import models

class tan_info(models.Model):
    tan_id = models.CharField(max_length=45, primary_key=True)
    area = models.CharField(max_length=45)
    group = models.CharField(max_length=45, blank=True, null=True)
    tan_name = models.CharField(max_length=45, unique=True)

class all_examinee_info(models.Model):
    exam_id = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45, primary_key=True)
    gender = models.CharField(max_length=45)
    personal_phone_number = models.CharField(max_length=45, blank=True, null=True)
    contact_person = models.CharField(max_length=45, blank=True, null=True)
    contact_person_num = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    tan_id = models.ForeignKey(tan_info, on_delete=models.CASCADE)
    tan_name = models.CharField(max_length=45)
    job = models.CharField(max_length=45)
    exam_date = models.CharField(max_length=45)
    exam_group = models.IntegerField()
    signed = models.CharField(max_length=45, blank=True, null=True)
    finished = models.CharField(max_length=45, blank=True, null=True)

class article_info(models.Model):
    article_id = models.CharField(max_length=45, primary_key=True)
    article_name = models.CharField(max_length=200)

class actual_exam_situation(models.Model):
    exam_id = models.ForeignKey(all_examinee_info, on_delete=models.CASCADE)
    article_id = models.ForeignKey(article_info, on_delete=models.CASCADE)
    correctness_minus = models.IntegerField(blank=True, null=True)
    fluency_minus = models.IntegerField(blank=True, null=True)
    final_score = models.IntegerField(blank=True, null=True)
    final_examiner = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45)

class exams(models.Model):
    exam_id = models.ForeignKey(all_examinee_info, on_delete=models.CASCADE)
    exam_date = models.CharField(max_length=45)
    exam_group = models.IntegerField()

class awards(models.Model):
    award_id = models.CharField(max_length=45, primary_key=True)
    article_id = models.ForeignKey(article_info, blank=True, null=True, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=200)