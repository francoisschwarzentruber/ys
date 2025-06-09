from django import forms

class SubmitReportForm(forms.Form):
    title = forms.CharField()
    pdf = forms.FileField()
    
class SubmitReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea)
    
    