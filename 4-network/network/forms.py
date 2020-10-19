from django import forms

from .models import Post

MAX_POST_LENGTH = 250 

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_POST_LENGTH:
            raise forms.ValidationError("This Post is too long")
        return content
