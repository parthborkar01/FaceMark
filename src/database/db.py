from src.database.config import supabase
import bcrypt

def check_teacher_exist(username):
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data) >0

def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")


def check_pass(password,hashpass):
    return bcrypt.checkpw(password.encode(), hashpass.encode("utf-8"))

def create_teacher(username,password,name):
    data = {"username":username,"password":hash_pass(password),"name":name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(usename,password):
    response = supabase.table("teachers").select("*").eq("username",usename).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password,teacher["password"]):
            return teacher
    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data = {'name':new_name,"face_embedding":face_embedding,"voice_embedding":voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data

def create_subject(sub_id,sub_name,sub_session,teacher_id):
    data = {"subject_code":sub_id,"name":sub_name,"section":sub_session,"teacher_id":teacher_id}
    response = supabase.table('subjects').insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response = supabase.table("subjects").select(
        "*,subject_students(count),attendance_logs(timestamp)"
    ).eq("teacher_id", teacher_id).execute()
    subjects = response.data or []
    for sub in subjects:
        student_counts = sub.get("subject_students", [])
        sub["total_students"] = student_counts[0].get("count", 0) if student_counts else 0
        attendance = sub.get("attendance_logs", [])
        unique_sessions = len({log.get("timestamp") for log in attendance if log.get("timestamp")})
        sub['total_classes'] = unique_sessions

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)
    return subjects


def enroll_student_to_subject(student_id,subject_id):
    data = {"student_id":student_id,"subject_id":subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id,subject_id):
    response = supabase.table('subject_students').delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table("subject_students").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data