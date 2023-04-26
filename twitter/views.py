from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
	if request.user.is_authenticated:
		form = TweetForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				tweet = form.save(commit=False)
				tweet.user = request.user
				tweet.save()
				messages.success(request, ("Your Tweet Has Been Posted!"))
				return redirect('home')
		profiles = Profile.objects.exclude(user=request.user)
		tweets = Tweet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"tweets":tweets, "form":form, "profiles": profiles})
	else:
		profiles = Profile.objects.all()
		tweets = Tweet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"tweets":tweets, "profiles": profiles})
	
def explore(request):	
	profiles = Profile.objects.all()
	tweets = Tweet.objects.all().order_by("-created_at")
	return render(request, 'explore.html', {"tweets":tweets, "profiles": profiles})


def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')


def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

		# Post Form logic
		if request.method == "POST":
			# Get current user
			current_user_profile = request.user.profile
			# Get form data
			action = request.POST['follow']
			# Decide to follow or unfollow
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			# Save the profile
			current_user_profile.save()



		return render(request, "profile.html", {"profile":profile, "tweets":tweets})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')		



def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out."))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
	
def tweet_like(request, pk):
	if request.user.is_authenticated:
		tweet = get_object_or_404(Tweet, id=pk)
		if tweet.likes.filter(id=request.user.id):
			tweet.likes.remove(request.user)
		else:
			tweet.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))




	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
	

def update_tweet(request, pk):
	if request.user.is_authenticated:
		tweet = get_object_or_404(Tweet, id=pk)

		if request.method == "POST":
			form = TweetForm(request.POST, instance=tweet)
			if form.is_valid():
				form.save()
				messages.success(request, ("Your Tweet Has Been Updated!"))
				return redirect('profile')
		
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('profile')

@login_required
def delete_tweet(request, pk):
	if request.user.is_authenticated:
		tweet = get_object_or_404(Tweet, pk=pk)
		if tweet.user == request.user:
			tweet.delete()
			messages.success(request, ("Your Tweet Has Been Deleted!"))
			return redirect('home')
		else:
			messages.success(request, ("You Must Be.."))
			return redirect('home')

	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')

		


