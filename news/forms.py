from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control mb-3",
                                          "name": "text",
                                          "id": "comment",
                                          "cols": "30",
                                          "rows": "5",
                                          "placeholder": "Комментарий"})
        }
