"""
Transformation logic for FEMA data.

Converts raw API records into a structured format
suitable for database insertion.
"""

from datetime import datetime


def parse_date(date_str: str):
    """
    Safely parse ISO date string.

    Args:
        date_str (str): Date string.

    Returns:
        date or None: Parsed date or None if invalid.
    """
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str).date()
    except Exception:
        return None


def transform_projects(projects: list) -> list:
    """
    Transform raw FEMA records into curated schema.

    Args:
        projects (list): Raw API records.

    Returns:
        list: Transformed project records.
    """
    transformed = []

    for p in projects:
        transformed.append(
            {
                "disaster_number": p.get("disasterNumber"),
                "state": p.get("state"),
                "county": p.get("county"),
                "incident_type": p.get("incidentType"),
                "declaration_date": parse_date(p.get("declarationDate")),
                "applicant_name": p.get("applicantName"),
                "project_number": p.get("projectNumber"),
                "project_title": p.get("projectTitle"),
                "federal_share": float(p.get("federalShareObligated") or 0),
                "total_obligated": float(p.get("totalObligated") or 0),
            }
        )

    return transformed
