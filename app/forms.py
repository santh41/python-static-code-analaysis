from django import forms

class GitHubURLForm(forms.Form):
    github_url = forms.URLField(label="GitHub Repository URL", required=True)
