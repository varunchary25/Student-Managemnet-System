from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from students.forms import StudentModelForm
from .models import Student

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def home(request):
    return render(request, 'students/home.html')


def student_list(request):
    students = Student.objects.all()

    return render(
        request,
        'students/student_list.html',
        {'students': students}
    )


@ensure_csrf_cookie
def student_register(request):

    if request.method == 'POST':

        form = StudentModelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentModelForm()

    return render(
        request,
        'students/student_form.html',
        {'form': form}
    )

@api_view(['GET'])
def student_api(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def student_detail_api(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['POST'])
def create_student_api(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_student_api(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def partial_update_student_api(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_student_api(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    student.delete()
    return Response({"message": "Student deleted successfully."}, status=200)

#authentication views
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard or home page after successful login
        else:
            return render(request, 'students/login.html', {'error': 'Invalid credentials'})
    return render(request, 'students/login.html')


@login_required
def dashboard(request):
    return render(request, 'students/dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to home page after logout

def save_student_name(request):
    request.session['student_name'] = request.POST.get('name')

    return render(request, "students/student_session.html")

def show_student_name(request):
    student_name = request.session.get('student_name', 'Guest')
    return render(request, "students/show_student_session.html", {'student_name': student_name})


# Common token authentication decorator
def token_protected(view_function):
    return authentication_classes([TokenAuthentication])(
        permission_classes([IsAuthenticated])(
            view_function
        )
    )


# GET: Display all students
@api_view(['GET'])
@token_protected
def student_api(request):

    students = Student.objects.all()

    serializer = StudentSerializer(
        students,
        many=True
    )

    return Response(serializer.data)


# GET: Display one student
@api_view(['GET'])
@token_protected
def student_detail_api(request, student_id):

    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=404
        )

    serializer = StudentSerializer(student)

    return Response(serializer.data)


# POST: Create student
@api_view(['POST'])
@token_protected
def create_student_api(request):

    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    return Response(serializer.errors, status=400)


# PUT: Update complete student details
@api_view(['PUT'])
@token_protected
def update_student_api(request, student_id):

    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=404
        )

    serializer = StudentSerializer(
        student,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# PATCH: Update selected student fields
@api_view(['PATCH'])
@token_protected
def partial_update_student_api(request, student_id):

    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=404
        )

    serializer = StudentSerializer(
        student,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# DELETE: Delete student
@api_view(['DELETE'])
@token_protected
def delete_student_api(request, student_id):

    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=404
        )

    student.delete()

    return Response(
        {'message': 'Student deleted successfully'},
        status=200
    )


# Protected API
@api_view(['GET'])
@token_protected
def protected_view(request):

    return Response({
        'message': 'Authentication successful!',
        'username': request.user.username
    })