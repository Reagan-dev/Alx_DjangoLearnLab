from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from .models import Article
from .forms import ArticleForm


# Create your views here.
@permission_required('articles.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

@permission_required('articles.can_create', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/create.html', {'form': form})

@permission_required('articles.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('article_list')
    return render(request, 'articles/edit.html', {'form': form, 'article': article})