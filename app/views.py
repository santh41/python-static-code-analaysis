import csv
import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import AnalysisResult
from .forms import GitHubURLForm
from .utils.github_clone import clone_repo
from .analysis.bandit_analysis import run_bandit_analysis
from .analysis.lizard_analysis import run_lizard_analysis
from .analysis.pylint_analysis import run_pylint_analysis
from .analysis.radon_analysis import run_radon_analysis

def analyze_repo(request):
    if request.method == "POST":
        form = GitHubURLForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["github_url"]
            repo_path = clone_repo(repo_url)

            analysis_results = [
                ("Pylint", run_pylint_analysis(repo_path)),
                ("Bandit", run_bandit_analysis(repo_path)),
                ("Lizard", run_lizard_analysis(repo_path)),
                ("Radon", run_radon_analysis(repo_path)),
            ]

            repo_name = repo_url.split("/")[-1]
            for tool, result in analysis_results:
                AnalysisResult.objects.create(repo_name=repo_name, analysis_type=tool, issue_count=len(result), details=json.dumps(result))

            return render(request, "results.html", {"repo_name": repo_name, "results": analysis_results})
    else:
        form = GitHubURLForm()

    return render(request, "index.html", {"form": form})
def download_csv(request):
    """Generate a structured CSV report of the analysis results."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="analysis_results.csv"'

    writer = csv.writer(response)
    writer.writerow(["Repository Name", "Analysis Type", "Issue Count", "Severity", "Line Number", "Message"])

    results = AnalysisResult.objects.all()
    unique_entries = set()  # Track unique issues to prevent duplicates

    for result in results:
        try:
            details = json.loads(result.details) if result.details.strip() else []
            
            # Ensure it's a list
            if isinstance(details, dict):
                details = [details]  # Convert to list if it's a single dictionary
            elif isinstance(details, str):
                details = json.loads(details)  # Convert JSON string to list
            
        except json.JSONDecodeError:
            details = []

        for issue in details:
            # Ensure issue is a dictionary before accessing keys
            if isinstance(issue, dict):
                severity = issue.get("SEVERITY", issue.get("severity", "N/A"))
                line_number = issue.get("loc", issue.get("line", "N/A"))
                message = issue.get("message", "N/A")
            else:
                severity, line_number, message = "N/A", "N/A", str(issue)

            # Create a unique tuple for tracking duplicates
            issue_entry = (result.repo_name, result.analysis_type, result.issue_count, severity, line_number, message)

            if issue_entry not in unique_entries:
                unique_entries.add(issue_entry)
                writer.writerow(issue_entry)

    return response
