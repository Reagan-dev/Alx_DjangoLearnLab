from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileForm




def register(request):
	if request.user.is_authenticated:
		return redirect('blog:profile')

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data['email']
			user.save()

			# Auto-login after registration (optional)
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			if user is not None:
				login(request, user)
				messages.success(request, 'Registration successful. Welcome!')
				return redirect('blog:profile')
			else:
				messages.info(request, 'Registration successful. Please log in.')
				return redirect('blog:login')
		else:
			form = RegistrationForm()
	else:
		form = RegistrationForm()

	return render(request, 'blog/register.html', {'form': form})



@login_required
def profile(request):
	# Ensure profile exists (in case signals didn’t run in some edge scenario)
	_ = getattr(request.user, 'profile', None)
	if _ is None:
		from .models import Profile
		Profile.objects.get_or_create(user=request.user)

	context = {
		'user_obj': request.user,
	}
	return render(request, 'blog/profile.html', context)



@login_required
def profile_edit(request):
	# Ensure profile exists
	_ = getattr(request.user, 'profile', None)
	if _ is None:
		from .models import Profile
		Profile.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			request.user.email = form.cleaned_data['email']
			request.user.save()
			request.user.profile.bio = form.cleaned_data.get('bio', '')
			request.user.profile.save()
			messages.success(request, 'Profile updated successfully.')
			return redirect('blog:profile')
		else:
			form = ProfileForm(initial={
				'email': request.user.email,
				'bio': getattr(request.user.profile, 'bio', ''),
			})
	else:
		form = ProfileForm(initial={
			'email': request.user.email,
			'bio': getattr(request.user.profile, 'bio', ''),
		})

	return render(request, 'blog/profile_edit.html', {'form': form})


def home(request):
    return render(request, 'blog/home.html')

