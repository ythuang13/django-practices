from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.


class NewTaskForm(forms.Form):
    tasks = forms.CharField(label="New Tasks")


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["tasks"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    else:
        return render(request, "tasks/add.html", {
            "form": NewTaskForm()
        })


def remove(request):
    if request.method == "POST":
        print(request.POST)
        if "remove" in request.POST:
            
            return HttpResponseRedirect(reverse("tasks:remove"))
    return render(request, "tasks/remove.html")
