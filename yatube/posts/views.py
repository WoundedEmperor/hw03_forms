from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .models import Post, Group, User

from .forms import PostForm


POST_NUM = 10


def index(request):
    post_list = Post.objects.all()  # .order_by('-pub_date')
    paginator = Paginator(post_list, POST_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group_none = get_object_or_404(Group, slug=slug)
    post_list = group_none.posts.all()  # .order_by('-pub_date')
    paginator = Paginator(post_list, POST_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # posts = (
    #     Post.objects.filter(group=group_none).order_by('-pub_date')[:POST_NUM]
    # )
    title = 'Посты сообщества.'
    context = {
        'group': group_none,
        'page_obj': page_obj,
        # 'posts': posts,
        'title': title,
    }
    return render(request, 'posts/group_list.html', context, slug)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = (
        author.posts.select_related('group', 'author').order_by('-pub_date')
    )
    paginator = Paginator(post_list, POST_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = post_list.count()
    context = {
        'author': author,
        'username': username,
        'post_count': post_count,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    post_text = post.text[:30]
    post_count = Post.objects.filter(author=post.author).count()
    author = post.author

    context = {
        'post_id': post_id,
        'post': post,
        'post_count': post_count,
        'post_text': post_text,
        'author': author,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Новый пост',
    }

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(instance=post)
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save(commit=False)
            return redirect('posts:post_detail', post_id)
        return render(
            request, template, {'form': form, 'is_edit': is_edit}
        )
    return render(request, template, context)
