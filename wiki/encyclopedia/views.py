from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown
from random import randint as ri
from random import seed


def index(request):
    if request.method == "POST":
        title = util.get_entry(request.POST.get('q'))

        if title is not None:
            return render(request, "encyclopedia/show_page.html", {
                "title": markdown.markdown(title)
            })
        else:
            title =  request.POST.get('q')
            entries = util.list_entries()
            entries = [entry for entry in entries if title.lower() in entry.lower()]
            return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def TITLE(request, title):
    title_name = title
    title = util.get_entry(title)
    if title is not None or title_name == 'random':
        if title_name == 'random':
            seed(ri(0,5000))
            entries = util.list_entries()
            title = entries[ri(0, (len(entries)-1))].strip()
            return HttpResponseRedirect(reverse('TITLE', args=(),
                kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/show_page.html", {
                "title": markdown.markdown(title)
            })

    else:
         return HttpResponseNotFound("Encyclopedia entry does not exist.")

def add(request):
    if request.method == "POST":
        title = util.get_entry(request.POST.get('z'))
        if title is not None:
            return HttpResponseNotFound("This page already exists.")
        else:
            title = request.POST.get('z')
            content = request.POST.get('q')
            if not content.startswith("#"):
                content = "#" + title +" \n" + content
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                })
    else:
        return render(request, "encyclopedia/add.html")
    

