"""
JSON Data Tool for the Voice AI Agent.
Loads the company credibility JSON report and extracts a comprehensive
text summary that can be injected into the LLM prompt.
"""

import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def load_json(filepath: str) -> dict:
    """
    Load and parse the JSON report file.
    
    Args:
        filepath: Path to the company_credibility_report.json file
    
    Returns:
        Parsed JSON as a Python dictionary
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON from {filepath}")
        return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON file: {e}")
        raise


def safe_get(data: dict, *keys, default: Any = "Not Available") -> Any:
    """
    Safely navigate nested dictionary keys.
    
    Args:
        data: The dictionary to navigate
        *keys: Sequence of keys to traverse
        default: Value to return if key path doesn't exist
    
    Returns:
        The value at the key path or the default
    """
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        elif isinstance(current, list) and isinstance(key, int) and key < len(current):
            current = current[key]
        else:
            return default
        if current is None:
            return default
    return current


def format_currency(amount) -> str:
    """Format a number as Indian currency (lakhs/crores)."""
    if amount is None or amount == "Not Available":
        return "Not Available"
    try:
        amount = float(amount)
        if amount >= 10000000:
            return f"₹{amount / 10000000:.2f} Crore"
        elif amount >= 100000:
            return f"₹{amount / 100000:.2f} Lakh"
        else:
            return f"₹{amount:,.0f}"
    except (ValueError, TypeError):
        return str(amount)


def get_company_data_summary(data: dict) -> str:
    """
    Extract a comprehensive text summary from the JSON data.
    This summary is injected into the LLM's system prompt so it
    can answer any question about the company.
    
    Args:
        data: The parsed JSON dictionary
    
    Returns:
        A formatted text summary of all key company information
    """
    sections = []
    
    # ─── 1. Company Basics ──────────────────────────────────────────────
    sections.append("=== COMPANY BASIC INFORMATION ===")
    sections.append(f"Company Name: {safe_get(data, 'name')}")
    sections.append(f"CIN / Entity ID: {safe_get(data, 'entityId')}")
    sections.append(f"PAN: {safe_get(data, 'pan')}")
    sections.append(f"GSTIN: {safe_get(data, 'gstin')}")
    sections.append(f"Company Type: {safe_get(data, 'type')}")
    sections.append(f"Entity Class: {safe_get(data, 'entityClass')}")
    sections.append(f"Status: {safe_get(data, 'status')}")
    sections.append(f"Date of Incorporation: {safe_get(data, 'dateOfIncorporation')}")
    sections.append(f"Date of GST Registration: {safe_get(data, 'dateOfRegistration', '$date') if isinstance(safe_get(data, 'dateOfRegistration'), dict) else safe_get(data, 'dateOfRegistration')}")
    sections.append(f"Industry: {safe_get(data, 'industry')}")
    sections.append(f"Sub-Industry: {safe_get(data, 'subIndustry')}")
    sections.append(f"Constitution of Business: {safe_get(data, 'constitutionOfBusiness')}")
    sections.append(f"Nature of Business: {', '.join(safe_get(data, 'natureOfBusiness')) if isinstance(safe_get(data, 'natureOfBusiness'), list) else safe_get(data, 'natureOfBusiness')}")
    sections.append(f"Turnover Slab: {safe_get(data, 'turnover')}")
    sections.append(f"City: {safe_get(data, 'city')}")
    sections.append(f"State: {safe_get(data, 'state')}")
    sections.append(f"PIN: {safe_get(data, 'pin')}")
    sections.append(f"Owner: {safe_get(data, 'owner')}")
    sections.append(f"Website: {safe_get(data, 'website')}")
    sections.append(f"Domain: {safe_get(data, 'domain')}")
    sections.append(f"Date of VAT Registration: {safe_get(data, 'dateOfVatRegistration')}")
    
    # ─── 2. Contact Information ─────────────────────────────────────────
    sections.append("\n=== CONTACT INFORMATION ===")
    phones = safe_get(data, 'phone')
    if isinstance(phones, list):
        sections.append(f"Phone Numbers: {', '.join(phones)}")
    
    emails = safe_get(data, 'email')
    if isinstance(emails, list):
        sections.append(f"Email Addresses: {', '.join(emails[:10])}")  # Limit to 10
        if len(emails) > 10:
            sections.append(f"  ... and {len(emails) - 10} more email addresses")
    
    addresses = safe_get(data, 'address')
    if isinstance(addresses, list) and addresses:
        sections.append(f"Primary Address: {addresses[0]}")
        sections.append(f"Total Registered Addresses: {len(addresses)}")
    
    # ─── 3. Management / Directors ──────────────────────────────────────
    sections.append("\n=== CURRENT MANAGEMENT / DIRECTORS ===")
    management = safe_get(data, 'management')
    if isinstance(management, dict):
        current = safe_get(management, 'current')
        if isinstance(current, list):
            sections.append(f"Total Current Directors/Officers: {len(current)}")
            for i, director in enumerate(current, 1):
                name = safe_get(director, 'name')
                designation = safe_get(director, 'designation')
                din = safe_get(director, 'din')
                email = safe_get(director, 'email')
                dob = safe_get(director, 'dateOfBirth')
                nationality = safe_get(director, 'nationality')
                tenure_start = safe_get(director, 'tenureBeginDate')
                status = safe_get(director, 'status')
                address = safe_get(director, 'address')
                sections.append(
                    f"  {i}. {name} - {designation} | DIN: {din} | "
                    f"Email: {email} | DOB: {dob} | Nationality: {nationality} | "
                    f"Appointed: {tenure_start} | Status: {status} | Address: {address}"
                )
        
        former = safe_get(management, 'former')
        if isinstance(former, list) and former:
            sections.append(f"\nTotal Former Directors/Officers: {len(former)}")
            # Show first 10 former directors to keep summary manageable
            for i, director in enumerate(former[:10], 1):
                name = safe_get(director, 'name')
                designation = safe_get(director, 'designation')
                din = safe_get(director, 'din')
                tenure_start = safe_get(director, 'tenureBeginDate')
                tenure_end = safe_get(director, 'tenureEndDate')
                status = safe_get(director, 'status')
                sections.append(
                    f"  {i}. {name} - {designation} | DIN: {din} | "
                    f"Tenure: {tenure_start} to {tenure_end} | Status: {status}"
                )
            if len(former) > 10:
                sections.append(f"  ... and {len(former) - 10} more former directors")
    
    # ─── 4. Ratings & Reviews ───────────────────────────────────────────
    sections.append("\n=== RATINGS & REVIEWS ===")
    sections.append(f"Google Rating: {safe_get(data, 'googleRating')} ({safe_get(data, 'googleRatingCount')} ratings)")
    sections.append(f"JustDial Rating: {safe_get(data, 'justdialRating')} ({safe_get(data, 'justdialRatingCount')} ratings, {safe_get(data, 'justdial_reviews')} reviews)")
    sections.append(f"TradeIndia Rating: {safe_get(data, 'tradeIndiaRating')} ({safe_get(data, 'tradeIndiaRatingCount')} ratings)")
    sections.append(f"IndiaMart Rating: {safe_get(data, 'indiaMartRating')} ({safe_get(data, 'indiaMartRatingCount')} ratings)")
    
    other_mp = safe_get(data, 'other_marketplaces')
    if isinstance(other_mp, dict):
        for platform, info in other_mp.items():
            if isinstance(info, dict):
                sections.append(f"{platform.title()} Rating: {safe_get(info, 'ratings')} ({safe_get(info, 'rating_count')} ratings, {safe_get(info, 'reviews')} reviews)")
    
    # ─── 5. Awards & Certificates ──────────────────────────────────────
    sections.append("\n=== AWARDS & CERTIFICATES ===")
    awards = safe_get(data, 'awards')
    if isinstance(awards, list):
        if awards:
            for award in awards:
                sections.append(f"  Award: {safe_get(award, 'name')} - {safe_get(award, 'description')}")
        else:
            sections.append("  No awards listed.")
    
    certs = safe_get(data, 'certificates')
    if isinstance(certs, list):
        if certs:
            for cert in certs:
                sections.append(f"  Certificate: {safe_get(cert, 'name')} (Type: {safe_get(cert, 'type')})")
        else:
            sections.append("  No certificates listed.")
    
    # ─── 6. Charges ─────────────────────────────────────────────────────
    charges = safe_get(data, 'charges')
    if isinstance(charges, list):
        sections.append(f"\n=== CHARGES ===")
        if charges:
            sections.append(f"Total Charges: {len(charges)}")
            for i, charge in enumerate(charges[:5], 1):
                sections.append(f"  {i}. {json.dumps(charge, default=str)[:200]}")
        else:
            sections.append("  No charges recorded.")
    
    # ─── 7. Alert List ──────────────────────────────────────────────────
    sections.append("\n=== ALERTS ===")
    alert_list = safe_get(data, 'alertList')
    if isinstance(alert_list, list):
        active_alerts = [a for a in alert_list if isinstance(a, dict) and a.get('exists') == True]
        inactive_alerts = [a for a in alert_list if isinstance(a, dict) and a.get('exists') == False]
        
        sections.append(f"Total Alerts Checked: {len(alert_list)}")
        sections.append(f"Active Alerts (exists=true): {len(active_alerts)}")
        sections.append(f"Clear Alerts (exists=false): {len(inactive_alerts)}")
        
        if active_alerts:
            sections.append("\nACTIVE ALERTS:")
            for alert in active_alerts:
                alert_name = safe_get(alert, 'alert')
                severity = safe_get(alert, 'severity')
                details = safe_get(alert, 'detailsAsPerSource')
                sections.append(f"  ⚠ {alert_name} | Severity: {severity}")
                if isinstance(details, list) and details:
                    for detail in details[:3]:
                        sections.append(f"    Detail: {json.dumps(detail, default=str)[:200]}")
        
        if inactive_alerts:
            sections.append("\nCLEAR (NO ISSUE) ALERTS:")
            for alert in inactive_alerts:
                alert_name = safe_get(alert, 'alert')
                severity = safe_get(alert, 'severity')
                sections.append(f"  ✓ {alert_name} | Severity: {severity} | Status: CLEAR")
    
    # ─── 8. Alert Summary ──────────────────────────────────────────────
    alert_summary = safe_get(data, 'alertSummary')
    if isinstance(alert_summary, dict):
        sections.append("\n=== ALERT SEVERITY SUMMARY ===")
        severity = safe_get(alert_summary, 'severity')
        if isinstance(severity, dict):
            for level, count in severity.items():
                sections.append(f"  {level.upper()}: {count}")
        
        mgmt_alerts = safe_get(alert_summary, 'details', 'managementAlerts')
        if isinstance(mgmt_alerts, list) and mgmt_alerts:
            sections.append(f"\nManagement-Related Alerts: {len(mgmt_alerts)}")
            for ma in mgmt_alerts[:5]:
                sections.append(f"  DIN: {safe_get(ma, 'din')} - Alerts: {safe_get(ma, 'alerts')}")
    
    # ─── 9. Opening Hours ──────────────────────────────────────────────
    hours = safe_get(data, 'openingHours')
    if isinstance(hours, dict):
        sections.append("\n=== OPENING HOURS ===")
        for day, time in hours.items():
            sections.append(f"  {day}: {time}")
    
    # ─── 10. Trust Seal & Marketplace Verification ──────────────────────
    trust_seal = safe_get(data, 'trust_seal')
    if isinstance(trust_seal, dict):
        sections.append("\n=== TRUST SEAL VERIFICATION ===")
        for platform, verified in trust_seal.items():
            status = "Verified" if verified else "Not Verified"
            sections.append(f"  {platform.title()}: {status}")
    
    # ─── 11. Google Reviews ────────────────────────────────────────────
    reviews = safe_get(data, 'google_reviews')
    if isinstance(reviews, list) and reviews:
        sections.append(f"\n=== GOOGLE REVIEWS ({len(reviews)} reviews) ===")
        for review in reviews[:5]:
            sections.append(
                f"  - {safe_get(review, 'author_name')}: "
                f"Rating {safe_get(review, 'rating')}/5 "
                f"({safe_get(review, 'relative_time_description')})"
            )
    
    return "\n".join(sections)
