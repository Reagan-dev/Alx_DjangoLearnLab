from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistrationForm, ProfileForm
from .models import Post
from .models import Comment
from .forms import CommentForm





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


# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  
    context_object_name = 'posts'
    ordering = ['-created_at']  # latest first

# Detail view of one post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
	

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post_id)
    else:
        form = CommentForm()
    return redirect('post_detail', pk=post_id)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})


