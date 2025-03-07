import csv
import json
import os
import pandas as pd
import datetime
from io import BytesIO
from collections import defaultdict
from django.shortcuts import render
from django.http import HttpResponse
from .models import AnalysisResult
from .forms import GitHubURLForm
from .utils.github_clone import clone_repo
from .analysis.bandit_analysis import run_bandit_analysis
from .analysis.lizard_analysis import run_lizard_analysis
from .analysis.pylint_analysis import run_pylint
from .analysis.radon_analysis import run_radon_analysis

def analyze_repo(request):
    """Handles GitHub repo analysis and stores results in the database."""
    if request.method == "POST":
        form = GitHubURLForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["github_url"]
            repo_path = clone_repo(repo_url)

            analysis_results = [
                ("Pylint", run_pylint(repo_path)),
                ("Bandit", run_bandit_analysis(repo_path)),
                ("Lizard", run_lizard_analysis(repo_path)),
                ("Radon", run_radon_analysis(repo_path)),
            ]

            repo_name = repo_url.split("/")[-1]
            for tool, result in analysis_results:
                AnalysisResult.objects.create(
                    repo_name=repo_name,
                    analysis_type=tool,
                    issue_count=len(result) if isinstance(result, list) else 0,
                    details=json.dumps(result)
                )

            return render(request, "results.html", {"repo_name": repo_name, "results": analysis_results})
    else:
        form = GitHubURLForm()
    return render(request, "index.html", {"form": form})

def flatten_detail(detail):
    """Ensures JSON details are correctly formatted for CSV."""
    if isinstance(detail, dict):
        return "; ".join([f"{key}: {value}" for key, value in detail.items()])
    elif isinstance(detail, list):
        return " | ".join([flatten_detail(item) for item in detail])
    return str(detail)

def generate_csv():
    """Generates a multi-sheet Excel report with summary and detailed analysis."""
    modules = ["Pylint", "Bandit", "Lizard", "Radon"]
    summary_data = {module: 0 for module in modules}
    detailed_data = {module: [] for module in modules}

    results = AnalysisResult.objects.all()

    for result in results:
        module = result.analysis_type
        if module not in modules:
            continue

        try:
            details = json.loads(result.details) if isinstance(result.details, str) else result.details
        except json.JSONDecodeError:
            continue  # Ignore invalid JSON

        # Skip Pylint errors related to missing files
        if module == "Pylint" and "Unable to load file" in result.details:
            continue

        # Update summary count
        summary_data[module] += result.issue_count

        # Prepare detailed data
        detailed_data[module].append({
            "Repository": result.repo_name,
            "Issue Count": result.issue_count,
            "Details": flatten_detail(details),
            "Created At": result.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    # Convert summary to DataFrame
    summary_df = pd.DataFrame([{"Module": mod, "Total Issues": count} for mod, count in summary_data.items()])

    # Create an Excel file
    file_path = "/var/tmp/code_analysis_report.xlsx"
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        for module, data in detailed_data.items():
            if data:
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=module, index=False)

    return file_path

def download_csv(request):
    """Django view to generate and download the CSV."""
    file_path = generate_csv()

    with open(file_path, "rb") as f:
        response = HttpResponse(
            f.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="code_analysis_report.xlsx"'
    return response
