from django.shortcuts import render
from .models import Blog
from django.contrib.auth import get_user_model
from .serializers import SimpleAuthorSerializer, UpdateUserProfileSerializer, UserInfoSerializer, UserRegistrationSerializer, BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

# import ML model
import os 
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# load model

# MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', )
# VECTORIZER_PATH = os.path.join(BASE_DIR, 'classifier/models/vectorizer.joblib')

# model = joblib.load(MODEL_PATH)

# vectorizer = joblib.load(VECTORIZER_PATH)


# def classify_new_news(request):
#     try:
#         # get unclassified blogs from the database.
#         unclassified_news = Blog.objects.filter(is_classfied=False)

#         if not unclassified_news.exists():
#             return JsonResponse({"message": "No unclassified news found"}, status=200)
        
#         classified_results = []

#         for blog in unclassified_news:
#             # combine title and body for classification
#             text = f"{blog.title} {blog.content}"

#             # preprocessing and classifiying the text.
#             cleaned_text = text.lower().strip() # adjust cleaning according to training model
#             # vectorized_text = vectorizer.transform([cleaned_text])
#             # prediction = model.predict(vectorized_text)[0]


#             # update the blog object
#             # blog.is_fake = prediction
#             blog.is_classfied = True
#             blog.save()

#             # update the author's is_fake field
#             # author = blog.author
#             # if prediction == True:
#             #     author.fakeCount += 1
#             #     if author.fakeCount >= 3:
#             #         author.is_fake = True
#             #     else:
#             #         author.is_fake = False
#             #     author.save()

#                 # user = get_user_model()
#                 # if blog.is_fake:
#                 #     user = User.objects.get(username=username)
#             # user_profile = request.user
#             # if prediction == "fake":
#             #     user_profile.is_fake = True
#             # else:
#             #     user_profile.is_fake = False
#             # user_profile.save() 



#              # Add result to the response
#             # classified_results.append({
#             #     "is_fake": blog.is_fake,
#             #     "title": blog.title,
#             #     "classification": prediction,
#             #     "updated_blog_model": blog,
#             #     "author": author,

#             # })

#         return JsonResponse({"classified_news": classified_results}, status=200)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

# # end of ML model class






# start of regular API classes
class BlogListPagination(PageNumberPagination):
    page_size= 3


# Create your views here.
@api_view(["GET"])
def blog_list(request):
    blogs = Blog.objects.all()
    paginator = BlogListPagination()
    paginated_blogs = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(paginated_blogs, many=True)
    return paginator.get_paginated_response(serializer.data)


# @api_view(['GET'])
# def blog_list(request):
#     blogs = Blog.objects.all()
#     serializer = BlogSerializer(blogs, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def get_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)



@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UpdateUserProfileSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user = request.user
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def create_blog(request):
#     serializer = BlogSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_blog(request, pk):
    user = request.user
    blog = Blog.objects.get(id=pk)
    if blog.author != user:
        return Response({"error": "You are not the author of this blog"}, status=status.HTTP_403_FORBIDDEN)
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["PUT"])
# def update_blog(request, pk):
#     blog = Blog.objects.get(id=pk)
#     serializer = BlogSerializer(blog, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    user = request.user 
    if blog.author != user:
        return Response({"error": "You are not the author of this blog"}, status=status.HTTP_403_FORBIDDEN)
    blog.delete()
    return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    username = user.username
    return Response({"username": username})


@api_view(['GET'])
def get_userinfo(request, username):
    User = get_user_model() # use this as reference
    user = User.objects.get(username=username) 
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)


@api_view(["GET"])
def get_user(request, email):
    User = get_user_model()
    try:
        existing_user = User.objects.get(email=email)
        serializer = SimpleAuthorSerializer(existing_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    





