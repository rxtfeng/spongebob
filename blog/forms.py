from django import forms

from blog.models import Message


class ContactForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['username', 'email', 'message']
