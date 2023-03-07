from fastapi import APIRouter
from models.student import Student
from config.database import connection
from schemas.student import student_entity, list_of_student_entity
from bson import ObjectId

student_router = APIRouter()


# Getting all students
@student_router.get('/students')
async def find_all_students():
    return list_of_student_entity(connection.local.student.find())


# Get one student with matching id
@student_router.get('/students/{student_id}')
async def find_student_by_id(student_id):
    return student_entity(connection.local.student.find_one({"_id": ObjectId(student_id)}))


@student_router.get('/greatness')
async def greater_is_you():
    return "Greatness is you!!"


# Creating a student
@student_router.post('/students')
async def create_student(student: Student):
    connection.local.student.insert_one(dict(student))
    return list_of_student_entity(connection.local.student.find())


# Update a student
@student_router.put('/students/{student_id}')
# Find the student and updata the data
async def update_student(student_id, student: Student):
    connection.local.student.find_one_and_update(
        {"_id": ObjectId(student_id)},
        {"$set": dict(student)}
    )
    return student_entity(connection.local.student.find_one({"_id": ObjectId(student_id)}))


# Delete a student
@student_router.delete('/student/{student_id}')
async def delete_student(student_id):
    # Find the student and deletes it and return the same student object
    return student_entity(connection.local.student.find_one_and_delete({"_id": ObjectId(student_id)}))
