from django.shortcuts import render
from django import forms

from . import util

from markdown2 import markdown
from random import randint

class SearchForm(forms.Form):
    searchquery = forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'}), label=False)

class NewForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea())

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            searchquery = form.cleaned_data["searchquery"]
            entries = util.list_entries()
            searchresults = []
            for entry in entries:
                if searchquery.lower() == entry.lower():
                    return render(request, "encyclopedia/entry.html", {
                        "entry": markdown(util.get_entry(searchquery)), 
                        "title": searchquery,
                        "form": SearchForm()
                    })
                elif (entry.lower()).startswith(searchquery.lower()):
                    searchresults.append(entry)
            if len(searchresults) == 0:
                return render(request, "encyclopedia/error.html", {
                "title": "Search Results",
                "error": "No matching entries were found!",
                "form": SearchForm()
            })
            return render(request, "encyclopedia/search.html", {
                "searchresults" : searchresults,
                "form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "form": SearchForm()
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })

def entry(request, title):
    if (util.get_entry(title)):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown(util.get_entry(title)), 
            "title": title,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "Page Not Found",
            "error": "Error: No entry found in the encyclopedia database!",
            "form": SearchForm()
        })

def new(request):
    if request.method == "POST":
        nform = NewForm(request.POST)
        if nform.is_valid():
            title = nform.cleaned_data["title"]
            content = nform.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "title": "Duplicate Entry",
                    "error": "Error: An existing encyclopedia entry for "+title+" already exists!",
                    "form": SearchForm()
                })
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "entry": markdown(util.get_entry(title)), 
                    "title": title,
                    "form": SearchForm()
                })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": SearchForm(),
            "nform": NewForm()
        })

def edit(request, title):
    if request.method == "POST":
        eform = EditForm(request.POST)
        if eform.is_valid():
            content = eform.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown(util.get_entry(title)), 
                "title": title,
                "form": SearchForm()
            })
    else:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", { 
            "title": title,
            "eform": EditForm(initial={'content': entry}),
            "form": SearchForm()
        })

def random(request):
    if request.method == "GET":
        entries = util.list_entries()
        ran_num = randint(0, len(entries) - 1)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown(util.get_entry(entries[ran_num])), 
            "title": entries[ran_num],
            "form": SearchForm()
        })




