# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm                        #import forms
from models import UserModel, SessionToken, PostModel, CommentModel, LikeModel, LoginModel      #import models
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.utils import timezone
from datetime import datetime                                                                   #import datetime module
from imgurpython import ImgurClient
from django .contrib import messages
'''
import sendgrid
import os
from sendgrid.helpers.mail import *
'''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                          #paths inside the project
CLIENT_ID='6a5b377b9218cba'                                                                     #CLIENT_ID
CLIENT_SECRET='84433116f9dd74f743003555ebe5d3f5dbde205f'                                        #CLIENT_SECRET
SENDGRID_API_KEY='SG.Lnyjda8zRf-RHkDYOT_U9A.KMXZ_8hMNMcsSYxP5MokbXu4_xiG66ez81trw-iEo'          #SENDGRID_API_KEY


#sinup view starts
def signup_view(request):
    if request.method == "POST":                                                               #POST request method
        time = datetime.now()
        form = SignUpForm(request.POST)                                                        #make a POST request
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()           #create a new record in the database

            messages.success(request, "thanks for joining us")
            return render(request, 'success.html')

            # return redirect('login/')
    else:
        form = SignUpForm()

    return render(request, 'index.html', {
        'time':datetime.now(),
        },{'form': form})
#sinup view ends


#login view starts
def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')                             # saving data to DB
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):                         #check if a user that exists with the username and password
                    token = SessionToken(user=user)                                 #create a session for the user
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')                                   # send the user to the /feeds/ page after log in
                    response.set_cookie(key='session_token', value=token.session_token)#insert the session id inside the cookie
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'  #error message
            else:
                     return HttpResponse("Invalid Login details")

    elif request.method == 'GET':
        form = LoginForm()


    response_data['form'] = form
    return render(request,'login.html',response_data)                              #request to login page
#login view ends


#post_view starts
def post_view(request):
    user = check_validation(request)                                                 #check validation for username and password

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')                                  # saving data to DB
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '/' + post.image.url)

                client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
                print"run"
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')                                                  #redirect to feed page

        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')                                                        #redirect to login page
#post_view ends


#feed_view starts
def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')
        print "post creation"
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
                print"like"
        return render(request, 'feed.html', {'posts': posts})
        print"feed page"
    else:

        return redirect('/login/')                                                  #redirect to login page
#feed_view starts


#like_view starts
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)

            else:
                existing_like.delete()
            return redirect('/feed/')                                             #redirect to feed page
    else:
        return redirect('/login/')                                                #redirect to login page
#like_view ends


#comment_view starts
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id                                       # saving data to DB
            comment_text = form.cleaned_data.get('comment_text')                             # saving data to DB
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()

            # email sending part ends
            return redirect('/feed/')                                                       #redirect to feed page
        else:
            return redirect('/feed/')                                                       #redirect to feed page
    else:
        return redirect('/login')                                                           #redirect to login page
# comment_view ends



#For validating the session or check validation
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None


