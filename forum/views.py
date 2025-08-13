from django.shortcuts import render
from django.http import HttpResponse

def thread_list(request):
    """Forum thread listing"""
    return render(request, 'forum/index.html', {
        'threads': [],
        'categories': [],
    })

def thread_detail(request, slug):
    """Thread detail view"""
    return render(request, 'forum/detail.html', {
        'thread': {'slug': slug, 'title': f'Thread {slug}'},
        'posts': [],
    })

def category_threads(request, slug):
    """Category threads view"""
    return HttpResponse(f"<h1>Threads in category: {slug}</h1>")

def create_thread(request):
    """Create new thread"""
    return HttpResponse("<h1>Create Thread</h1><p>Thread creation form.</p>")

def add_post(request, slug):
    """Add post to thread"""
    return HttpResponse(f"<h1>Add Post to {slug}</h1><p>Post creation form.</p>")