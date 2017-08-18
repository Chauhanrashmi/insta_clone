# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json                                                                                  #saving of Base_URL in global variables
from django.shortcuts import render, redirect, render_to_response,HttpResponseRedirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm ,UpvoteForm           #import forms
from models import UserModel, SessionToken, PostModel, CommentModel, LikeModel, LoginModel    #import models
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.utils import timezone
from datetime import datetime                                                                   #import datetime module
from imgurpython import ImgurClient
from django .contrib import messages
import sendgrid
from sendgrid.helpers import mail
from django.contrib.auth.views import logout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                          #paths inside the project
CLIENT_ID='6a5b377b9218cba'                                                                     #CLIENT_ID
CLIENT_SECRET='84433116f9dd74f743003555ebe5d3f5dbde205f'                                        #CLIENT_SECRET



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
            user.save()                                                                    #create a new record in the database
            # email sending part starts
            sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
            from_email = Email("chauhanrashmi1998@gmail.com.")
            to_email = Email(email)
            subject = "Successfully signed up."
            content = Content("text/plain", "Welcome to smart kids instagram app! enjoy your app")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            # email sending part ends
            return render(request, 'success.html')
        else:
            messages.warning(request, "Error:Please fill all fields correctly!")

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
            password = form.cleaned_data.get('password')                               # saving data to DB
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):                            #check if a user that exists with the username and password
                    token = SessionToken(user=user)                                    #create a session for the user
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')                                      # send the user to the /feeds/ page after log in
                    response.set_cookie(key='session_token', value=token.session_token)#insert the session id inside the cookie
                    return response
                else:
                    response_data['message'] = 'Error:Incorrect Username/Password combination.! Please try again!'   #error message
                    messages.warning(request, "Error:Incorrect Username/Password combination.! Please try again!")
            else:
                messages.warning(request, "Error:User does not exist with provided Login details!Please try again!")
                return render(request, 'login.html', response_data)

        else:
            messages.warning(request, "Error:Please provide correct Login details in all fields above")

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
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()
                messages.success(request, "Hey!Post Sucessfully Created!")
                return redirect('/feed/')                                                  #redirect to feed page
            else:
                messages.warning(request, "Error:Post could not be created now.Please try again later!")
        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        messages.warning(request, "Error:Please fill Login details first!")
        return redirect('/login/')                                                        #redirect to login page
#post_view ends


#feed_view starts
def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        messages.warning(request, "Error:Please fill Login details first!")
        return redirect('/login/')                                                  #redirect to login page
#feed_view ends


#like_view starts
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            print "liked"
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                # email sending part starts
                postget = PostModel.objects.filter(id=post_id).first()
                userid = postget.user_id
                user = UserModel.objects.filter(id=userid).first()
                email = user.email
                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
                from_email = Email("chauhanrashmi1998@gmail.com.")
                to_email = Email(email)
                subject = "someone likes your post!"
                content = Content("text/plain", " Your  post is liked")
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                # email sending part ends
                print"like"
                messages.success(request, "Yepee!Post Sucessfully liked!")
            else:
                existing_like.delete()
                messages.success(request, "Yeww!Post Sucessfully Unliked!")
            return redirect('/feed/')                                                    #redirect to feed page
    else:
        messages.warning(request, "Error:Please fill Login details first!")
        return redirect('/login/')                                                        #redirect to login page
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

            # email sending part starts
            postget = PostModel.objects.filter(id=post_id).first()
            userid = postget.user_id
            user = UserModel.objects.filter(id=userid).first()
            email = user.email
            sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
            from_email = Email("chauhanrashmi1998@gmail.com.")
            to_email = Email(email)
            subject = "Someone left a comment on your post!"
            content = Content("text/plain", "comments are posted by someone")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            return redirect('/feed/')
            # email sending part ends
            messages.success(request, "Wow!Comment Sucessfully posted!")
            return redirect('/feed/')                                                       #redirect to feed page
        else:
            messages.warning(request, "Error:Comment can not be posted now.Please try again later !")
            return redirect('/feed/')                                                       #redirect to feed page
    else:
        messages.warning(request, "Error:Please fill Login details first!")
        return redirect('/login')                                                           #redirect to login page
# comment_view ends


# upvote_view starts
def upvote_view(request):
    user = check_validation(request)
    comment = None
    if user and request.method == 'POST':
        form = UpvoteForm(request.POST)
        if form.is_valid:
            print form.cleaned_data
            comment_id = int(form.cleaned_data.get('id'))
            comment = CommentModel.objects.filter(id = comment_id).first()
            if comment is not None:
                comment.upvote_number+= 1
                comment.save()
                print comment.upvote_number
                messages.success(request,'Comment successfully upvoted!')
                return redirect('/feed/')
            else:
                messages.success(request, 'ERROR:SOME ERROR!')
                return redirect('/login/')
        else:
            messages.warning(request, "Error:Comment can not be upvoted now.Please try again later !")
            return redirect('/feed/')
    else:
        messages.warning(request, "Error:Please fill Login details first!")
        return redirect('/login')
# upvote_view ends


# logout_view starts
def logout_view(request):
    user = check_validation(request)
    if user is not None:
        session_id = SessionToken.objects.filter(user=user).last()
        if session_id:
            session_id.delete()
    return render(request,'login.html')
    messages.success(request, "Sucessfully logged out, please login to continue!")
# logout_view ends


#Function declaration to get the recent post of a user by username and returns the id of the most recent image starts



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