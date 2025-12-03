from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        from main_app.models import Course, Session, Staff, Student
        from datetime import date

        # 1. Create Admin
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(email=email).exists():
            self.stdout.write(f'Creating superuser {email}...')
            User.objects.create_superuser(email=email, password=password, user_type='1')
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully!'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {email} already exists. Updating password...'))
            u = User.objects.get(email=email)
            u.set_password(password)
            u.save()
            self.stdout.write(self.style.SUCCESS(f'Password for {email} updated.'))

        # 2. Create Demo Course & Session (Required for Staff/Student)
        course, _ = Course.objects.get_or_create(name="Computer Engineering")
        session, _ = Session.objects.get_or_create(start_year=date(2023, 1, 1), end_year=date(2027, 1, 1))

        # 3. Create Demo Staff
        staff_email = "staff@example.com"
        if not User.objects.filter(email=staff_email).exists():
            self.stdout.write(f'Creating staff user {staff_email}...')
            user = User.objects.create_user(email=staff_email, password='staff123', user_type='2', first_name='Demo', last_name='Staff')
            self.stdout.write(self.style.SUCCESS(f'Staff {staff_email} created successfully!'))
        else:
            self.stdout.write(f'Staff user {staff_email} already exists. Checking profile...')
            user = User.objects.get(email=staff_email)
        
        # Ensure Staff profile exists and is linked to course
        if not Staff.objects.filter(admin=user).exists():
            self.stdout.write(f'Creating missing profile for {staff_email}...')
            Staff.objects.create(admin=user, course=course)
        else:
            staff = Staff.objects.get(admin=user)
            staff.course = course
            staff.save()

        # 4. Create Demo Student
        student_email = "student@example.com"
        if not User.objects.filter(email=student_email).exists():
            self.stdout.write(f'Creating student user {student_email}...')
            user = User.objects.create_user(email=student_email, password='student123', user_type='3', first_name='Demo', last_name='Student')
            self.stdout.write(self.style.SUCCESS(f'Student {student_email} created successfully!'))
        else:
            self.stdout.write(f'Student user {student_email} already exists. Checking profile...')
            user = User.objects.get(email=student_email)

        # Ensure Student profile exists and is linked to course/session
        if not Student.objects.filter(admin=user).exists():
            self.stdout.write(f'Creating missing profile for {student_email}...')
            Student.objects.create(admin=user, course=course, session=session)
        else:
            student = Student.objects.get(admin=user)
            student.course = course
            student.session = session
            student.save()
