from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .models import User
from .serializer import UserSerializer

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return Response(data,status=status.HTTP_200_OK)

class UserDetailByUsernameAPIView(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    def get(self, request, username):
        user = self.get_object(username)
        if not user:
            return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class UserListAPIViewQueryParam(APIView):
    def get(self, request):
        qs = User.objects.all()

        #Filters
        min_age = request.GET.get('min_age')
        max_age = request.GET.get('max_age')
        if min_age is not None:
            qs = qs.filter(age__gte=min_age)
        if max_age is not None:
            qs = qs.filter(age__lte=max_age)
        
        #Ordering (e. g., ?ordering=username or ?ordering=-created_at)
        ordering = request.GET.get('ordering') or '-created_at'
        qs = qs.order_by(ordering)

        #Simple pagination
        page_size = int(request.GET.get('page_size', 10))
        page = int(request.GET.get('page',1))
        start = (page - 1)* page_size
        end = start + page_size
        total = qs.count()

        data = UserSerializer(qs[start:end], many = True).data

        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'results': data
        }, status=status.HTTP_200_OK)