from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.baseconv import base64

from .models import shorturl
import random
import string


# Create your views here.


@login_required(login_url='/login/')
def dashboard(request):
    usr = request.user
    urls = shorturl.objects.filter(user=usr)
    return render(request, 'dashboard.html', {'urls': urls})


@login_required(login_url='/login/')
def generate(request):
    if request.method == "POST":
        # generate
        pass
        if request.POST['original']:
            # generate randomly
            usr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = __fnv_hash(original)
                check = shorturl.objects.filter(short_query=short)
                if not check:
                    newurl = shorturl(
                        user=usr,
                        original_url=original,
                        short_query=short,
                    )
                    newurl.save()
                    return redirect(dashboard)
                else:
                    continue
        else:
            messages.error(request, "Empty Fields")
            return redirect(dashboard)
    else:
        return redirect('/dashboard')


def home(request, query=None):
    if not query or query is None:
        return render(request, 'home.html')
    else:
        try:
            check = shorturl.objects.get(short_query=query)
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except shorturl.DoesNotExist:
            return render(request, 'home.html', {'error': "error"})


# added delete URl


@login_required(login_url='/login/')
def deleteurl(request):
    if request.method == "POST":
        short = request.POST['delete']
        try:
            check = shorturl.objects.filter(short_query=short)
            check.delete()
            return redirect(dashboard)
        except shorturl.DoesNotExist:
            return redirect(home)
    else:
        return redirect(home)


def __fnv_hash(key):
    h = 2166136261

    for k in key:
        h = (h * 16777619) ^ ord(k)

    # Return 8 bit URL
    return base64.encode(h % 281474976710656)
