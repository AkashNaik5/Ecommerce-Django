from django.shortcuts import render
from django.http import HttpResponse
from .models import  Blogpost


def index(request):
    blogs = Blogpost.objects.all()
    return render(request, 'blog/index.html', {'blogs': blogs})


def blogpost(request, id):
    blog = Blogpost.objects.filter(post_id=id)[0]
    print(blog)
    return render(request, 'blog/blogpost.html', {'blog': blog})


def searchMatch(query, item):
    print(item.blog_desc)
    if query in item.blog_desc.lower() or query in item.blog_title.lower() or \
             query in item.heading0.lower() or query in item.content0.lower() or \
            query in item.heading1.lower() or query in item.content1.lower() or query in item.heading2.lower() or \
            query in item.content2.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allblogs = []
    blogs = Blogpost.objects.values('blog_title', 'post_id')
    ids = {item['post_id'] for item in blogs}
    itmes = []
    for id in ids:
        blog = Blogpost.objects.filter(post_id = id)
        item = [item for item in blog if searchMatch(query, item)]
        if len(item)>0:
            itmes.append(item)
    print("result",itmes)
    result = []
    for x in itmes:
        result.append(x[0])
    print("result",result)
    return render(request, 'blog/index.html', {'blogs': result})