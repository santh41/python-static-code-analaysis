import csv
from django.http import HttpResponse
from .models import AnalysisResult

def generate_csv_report(repo_name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{repo_name}_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Analysis Tool", "Issue Count", "Details"])
    
    results = AnalysisResult.objects.filter(repo_name=repo_name)
    for result in results:
        writer.writerow([result.analysis_type, result.issue_count, result.details])
    
    return response
