#import the necessary modules
from pymongo import MongoClient
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.garywk6.mongodb.net/?retryWrites=true&w=majority")
db = client.db_git
teachers = db.teachers
students = db.students

#enroll Teachers
def teacherEnroll(name:str,id:int,department:str):
    query = {
    'name':name,
    'id':id,
    'department':department
    }
    teachers.insert_one(query)


#enroll students
def studentsEnroll(name:str,age:int,id:int,Class:str,state:str,role:str):
    query =  {
    'name':name,
    'age':age,
    'id':id,
    'class':Class,
    'state':state,
    'role':role,
    'present': [],
    'daysPresent':0,
    'absent':[],
    'daysAbsent':0
    }
    students.insert_one(query)
