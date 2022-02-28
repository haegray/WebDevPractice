from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import util
import markdown


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
    title = util.get_entry(title)
    if title is not None:
        return render(request, "encyclopedia/show_page.html", {
            "title": markdown.markdown(title)
        })
    else:
         return HttpResponseNotFound("Encyclopedia entry does not exist.")

