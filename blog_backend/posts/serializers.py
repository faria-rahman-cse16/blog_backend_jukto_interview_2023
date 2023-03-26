from rest_framework import serializers
from .models import Post,Comment,Coustomer


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coustomer
        fields = '__all__'
		
		
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.name')
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.name')
    class Meta:
        model = Comment
        fields = '__all__'