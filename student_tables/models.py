from django.db import models



class Student(models.Model):
    id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    DOB = models.DateField()


class Department(models.Model):
    department_code = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    faculty = models.CharField(max_length=50)


class Degree(models.Model):
    title = models.CharField(max_length=50)
    degree_code = models.IntegerField(primary_key = True)
    department_code_id = models.ForeignKey(Department, on_delete=models.CASCADE)


class Register(models.Model):
    id = models.AutoField(primary_key = True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    degree_id = models.ForeignKey(Degree, on_delete=models.CASCADE)
    year = models.DateField()
    

class Course(models.Model):
    course_code = models.IntegerField(primary_key=True)
    course_title = models.CharField(max_length=50)
    hours = models.FloatField()


class Takes(models.Model):
    course_reg_number = models.IntegerField(primary_key=True)
    course_code_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.DateField()


class Requires(models.Model):
    id = models.AutoField(primary_key=True)
    course_code_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    degree_id = models.ForeignKey(Degree, on_delete=models.CASCADE)