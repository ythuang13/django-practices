from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import markdown2
from random import choice

from . import util
from .forms import EntryForm


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


markdowner = markdown2.Markdown()


def get_entry(request, title: str):
    page = util.get_entry(title)

    if page:
        title = page.split("\n")[0].replace("# ", "").strip()
        return render(
            request,
            "encyclopedia/entry.html",
            {"title": title, "page": markdowner.convert(page)},
        )
    else:
        return HttpResponseRedirect(
            reverse(
                "encyclopedia:error",
                kwargs={
                    "title": "Page Not Found",
                },
            )
        )


def get_random(request):
    get_entry(request, choice(util.list_entries()))
    return HttpResponseRedirect(
        reverse("encyclopedia:entry", kwargs={"title": choice(util.list_entries())})
    )


def search(request):
    search_parameter: str = request.GET.get("q", "")
    if util.get_entry(search_parameter):
        return HttpResponseRedirect(
            reverse("encyclopedia:entry", kwargs={"title": search_parameter})
        )

    search_result = []
    for entry in util.list_entries():
        if search_parameter.lower() in entry.lower():
            search_result.append(entry)

    return render(
        request,
        "encyclopedia/search.html",
        {"searched": search_parameter, "results": search_result},
    )


def new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get("title", "")
            body = data.get("body", "")

            if title.lower() in [x.lower() for x in util.list_entries()]:
                return render(
                    request,
                    "encyclopedia/new.html",
                    {"form": form, "error_message": f"page, {title}, exists already"},
                )

            # success, save entry
            util.save_entry(title, bytes(body, "utf-8"))
            return HttpResponseRedirect(
                reverse("encyclopedia:entry", kwargs={"title": title})
            )
    else:
        form = EntryForm()
        return render(request, "encyclopedia/new.html", {"form": form})

    return render(
        request,
        "encyclopedia/new.html",
        {"form": form, "error_message": "Both fields are required!"},
    )


def edit_entry(request, title: str):
    if request.method == "POST":
        data = request.POST
        title = data.get("title", "")
        body = data.get("body", "")
        print(data)

        if body == "":
            return render(
                request,
                "encyclopedia/edit.html",
                {
                    "old_content": util.get_entry(title),
                    "error_message": "Content can't be left blank!",
                },
            )

        # success, save entry
        util.save_entry(title, bytes(body, "utf-8"))
        return HttpResponseRedirect(
            reverse("encyclopedia:entry", kwargs={"title": title})
        )

    print(repr(util.get_entry(title)))
    return render(
        request,
        "encyclopedia/edit.html",
        {"title": title, "old_content": util.get_entry(title)},
    )


def error(request, title):
    return render(request, "encyclopedia/error.html", {"title": title})
