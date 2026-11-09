from rest_framework.decorators import(
    api_view,
    authentication_classes,
    permission_classes  
)

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer

#GET: Display all students
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def student_list_api(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

#POST: Create a new student
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def student_create_api(request):

    serializer = StudentSerializer(data=request.data)    
    
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


#DELETE: Delete a student
@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def student_delete_api(request, student_id):
    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:

        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    student.delete()
    return Response({"message": "Student deleted successfully"}, status=status.HTTP_200_OK)
