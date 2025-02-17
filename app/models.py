#from django.db import models

# Create your models here.
from django.db import models

class AnalysisResult(models.Model):
    repo_name = models.CharField(max_length=255)
    analysis_type = models.CharField(max_length=50)  # Pylint, Bandit, etc.
    issue_count = models.IntegerField()
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
