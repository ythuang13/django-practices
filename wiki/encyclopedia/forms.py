from django import forms


class EntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", max_length=100, widget=forms.TextInput(attrs={"class": "ne_title_input"}))
    body = forms.CharField(
        label="Markdown Content:", widget=forms.Textarea(attrs={"class": "ne_text_body"})
    )
