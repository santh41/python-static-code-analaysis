from django.urls import path
from .views import analyze_repo, download_csv

urlpatterns = [
    path("", analyze_repo, name="home"),  # Default route
    path("analyze/", analyze_repo, name="analyze"),
    path("download-report/", download_csv, name="download_csv"),  # New route for CSV download
]
