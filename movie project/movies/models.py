from django.db import models
from django.conf import settings
# 게시판 모델
class Movie(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #유저정보 받아오기
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies') # 좋아요 기능
    title = models.CharField(max_length=20)         #제목
    image = models.ImageField(blank=True, null=True)  #이미지 첨부
    created_at = models.DateTimeField(auto_now_add=True)  #생성날짜
    updated_at = models.DateTimeField(auto_now=True)   #수정날짜
    description = models.TextField()     #내용

    def __str__(self):
            return f'{self.id}번째글 - {self.title}'

# 댓글 모델
class Comment(models.Model):  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content =models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    

# ManyToManyField , 중계테이블 생성방법

# class Doctor(models.Model):
#     name =models.TextField()

#     def __str__(self):
#         return f"{self.name} 전문의"

# class Patient(models.Model):
#     # doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE) #방법1
#     # doctors = models.ManyToManyField(Doctor,related_name='patients')  #방법3 = 방법2랑 같다, related_name은 역참조용-사용시 _set사용이 안된다.
#     doctors = models.ManyToManyField(Doctor, through='Reservation')
#     name = models.TextField()

#     def __str__(self):
#         return f"{self.pk}번 환자 {self.name}"

# class Reservation(models.Model): #중계테이블 #방법2
#     doctor =models.ForeignKey(Doctor,on_delete=models.CASCADE)
#     patient= models.ForeignKey(Patient,on_delete=models.CASCADE)
#     symptom = models.TextField() #증상
#     reserved_at =models.DateTimeField(auto_num_add =True) #예약날짜

#     def __str__(self):
#         return f"{self.doctor_id}번 의사의 {self.patient_id}번 환자" 