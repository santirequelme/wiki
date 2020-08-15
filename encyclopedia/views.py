from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
import random as RandomInt
markdowner = Markdown()


class addForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput)
    info = forms.CharField(label="", widget=forms.Textarea (attrs={'cols': 150}))

def entry(request, title):
    entries = util.get_entry(title)
    if entries is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entries),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    ent = util.list_entries()
    title = request.POST["title"]
    if title in ent:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    else:
        entry_match = []
        for entry in ent:
            if title.lower() in entry.lower():
                entry_match.append(entry)
        return render(request, "encyclopedia/search.html", { "entries":entry_match, "result": title, "found": len(entry_match)
        })

def create(request):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["info"]
            if title not in util.list_entries():
                util.save_entry(title, info)
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            else:
                infotext = {
                    'form': addForm(),
                    'message': f"{title} already exists."
                }
            return render(request, "encyclopedia/create.html", infotext)
    else:
        infotext = {
            'form': addForm()
        }
        return render(request, "encyclopedia/create.html", infotext)

def edit(request, title):
    if request.method == "POST":
        info = request.POST['info']
        util.save_entry(title, info)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    else:
        form_content = {
            "title": title,
            "info": util.get_entry(title)
        }
        return render(request, "encyclopedia/edit.html", form_content)

def random(request):
    all_entries = util.list_entries()
    title_rand = all_entries[RandomInt.randint(0, len(all_entries) - 1)]
    return HttpResponseRedirect(reverse("entry", kwargs={'title': title_rand}))














