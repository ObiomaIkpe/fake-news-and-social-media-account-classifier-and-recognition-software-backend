from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'is_fake', 'fake_count']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        # profile_picture_url = validated_data["profile_picture_url"]

        user = get_user_model()
        new_user = user.objects.create(email=email, username=username, first_name=first_name, last_name=last_name)

        new_user.set_password(password)
        new_user.save()

        return new_user
    


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name", "bio", "profile_picture" ]


class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "profile_picture", "profile_picture_url"]



    

class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializer(read_only=True)
    author_id = serializers.IntegerField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'author', 'slug', 'category', 'content', 'featured_image', 'created_at', 'updated_at', "author_id", 'is_draft', 'is_fake', 'published_date']


class UserInfoSerializer(serializers.ModelSerializer):
    author_posts = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name", "job_title", "bio", "profile_picture", "author_posts", "profile_picture_url"]

    
    def get_author_posts(self, user):
        blogs = Blog.objects.filter(author=user)[:9]
        serializer = BlogSerializer(blogs, many=True)
        return serializer.data
        
        
        

        

        
