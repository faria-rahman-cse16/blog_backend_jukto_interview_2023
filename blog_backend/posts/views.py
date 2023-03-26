from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Post, Comment, Coustomer
from .serializers import PostSerializer, CommentSerializer, UsersSerializer
from rest_framework import generics
from .permissions import IsModeratorOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
#from rest_framework.decorators import api_view
from rest_framework import filters



class PostListSearch(generics.ListAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =['user__name','title','body']
	

class UsersViewset(APIView):
    queryset = Coustomer.objects.all()
    serializer_class = UsersSerializer
    def get(self, request):
        users = Coustomer.objects.all()
        serializer = UsersSerializer(users, many = True)
        authentication_classes= [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UsersSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)	
       

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
	
	
class PostDetailModerators(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsModeratorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    

class UserPostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        user = Coustomer.objects.filter(name = name).first()
        if user is None:
            return Response({'error': 'User not found'}, status = status.HTTP_404_NOT_FOUND)
        posts = Post.objects.filter(user = user)
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

        


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            return None
    
    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post = post)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user.id,
            'post': post.id,
            'body': request.data.get('body')
        }
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)




