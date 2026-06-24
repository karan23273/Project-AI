from src.database.config import supabase
import bcrypt

def check_teacher_exist(teacher_user_name):
    # Check unique users returns false if user already exist
    response = supabase.table("teacher").select("teacher_user_name").eq('teacher_user_name', teacher_user_name).execute()
    return len(response.data) > 0

def hash_pass(user_password):
    return bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()

def match_pass(hashed, user_password):
    return bcrypt.checkpw(user_password.encode(), hashed.encode())

def create_teacher(teacher_user_name, teacher_name, teacher_user_pass):
    data ={
        'teacher_user_name': teacher_user_name,
        'teacher_pass': hash_pass(teacher_user_pass),
        'teacher_name' : teacher_name
    }
    response = supabase.table('teacher').insert(data).execute()
    return response.data

def teacher_login(teacher_user_name, teacher_user_pass):
    response = supabase.table('teacher').select('*').eq('teacher_user_name', teacher_user_name).execute()

    if response.data:
        teacher = response.data[0]
        if match_pass(teacher['teacher_pass'], teacher_user_pass):
            return teacher
    
    return None

def get_all_students():
    response = supabase.table('student').select('*').execute()
    return response.data

def create_student(name, user_name, face_embedding=None, voice_embedding=None):
    data={
        'student_name': name,
        'student_user_name': user_name,
        'face_embedding': face_embedding,
        'voice_embedding': voice_embedding
    }
    response = supabase.table('student').insert(data).execute()
    return response.data

def create_subject(teacher_id, course_code, course_name, course_section):
    data={
        'subject_name': course_name,
        'subject_code': course_code,
        'section': course_section,
        'teacher_id': teacher_id
    }
    response = supabase.table('subject').insert(data).execute()
    return response.data 

def get_teacher_subject(teacher_id):
    response = supabase.table('subject').select('*, subject_students(count), attendance_log(timestamp)').eq('teacher_id', teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_log', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_students', None)
        sub.pop('attendance_log', None)

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {
        'student_id': student_id,
        'subject_id': subject_id
    }
    response = supabase.table('subject_students').insert(data).execute()
    return response.data
def unenroll_student_from_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data

def get_student_subjects(student):
    response = supabase.table('subject_students').select('*, subject(*)').eq('student_id', student['student_id']).execute()
    return response.data

def get_student_attendance(student):
    response = supabase.table('attendance_log').select('*, subject(*)').eq('student_id', student['student_id']).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_log').insert(logs).execute()
    return response.data