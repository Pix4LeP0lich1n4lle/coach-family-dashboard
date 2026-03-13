#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to send personalized coaching dashboard access emails to all participants.
Uses SMTP credentials from .env or .connexion file.
"""

import smtplib
import sys
import os
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

# Participant data: name, email, token, dashboard URL
PARTICIPANTS = [
    {
        "name": "Joseph Delorey",
        "email": "jdelorey02@proton.me",
        "token": "joseph_coach_secret_x7k2m9n",
        "dashboard_url": "https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/coaching/index.html?token=joseph_coach_secret_x7k2m9n"
    },
    {
        "name": "Marie Giguère",
        "email": "mariegiguere@hotmail.ca",
        "token": "marie_coach_secret_q4b8r1p",
        "dashboard_url": "https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/coaching/index.html?token=marie_coach_secret_q4b8r1p"
    },
    {
        "name": "Alex Delorey",
        "email": "alexdelorey21@icloud.com",
        "token": "alex_coach_secret_w9d3f5t",
        "dashboard_url": "https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/coaching/index.html?token=alex_coach_secret_w9d3f5t"
    },
    {
        "name": "Chantal Felteau",
        "email": "felteau@gmail.com",
        "token": "chantal_coach_secret_h7j2l8v",
        "dashboard_url": "https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/coaching/index.html?token=chantal_coach_secret_h7j2l8v"
    },
    {
        "name": "Danielle Delorey",
        "email": "deloreydanielle@hotmail.com",
        "token": "danielle_coach_secret_z6c4m1x",
        "dashboard_url": "https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/coaching/index.html?token=danielle_coach_secret_z6c4m1x"
    }
]


def load_credentials():
    """Load SMTP credentials from .connexion file."""
    # Fall back to .connexion file
    cred_path = Path.home() / "ai-lab" / "PROJECTS" / "Coach_Suivies" / ".credentials" / ".connexion"

    if not cred_path.exists():
        print(f"❌ Credentials file not found: {cred_path}")
        sys.exit(1)

    content = cred_path.read_text()
    lines = content.split('\n')

    email = None
    app_password = None
    in_credentials_section = False

    for line in lines:
        # Don't strip yet - preserve spaces in values
        stripped = line.strip()

        if stripped == '[CREDENTIALS]':
            in_credentials_section = True
            continue

        if stripped.startswith('[') and stripped != '[CREDENTIALS]':
            in_credentials_section = False
            continue

        if in_credentials_section and '=' in stripped:
            key, value = stripped.split('=', 1)
            key = key.strip()
            value = value.strip()

            if key == 'Email':
                email = value
            elif key == 'App Password':
                app_password = value

    if not email or not app_password:
        print(f"❌ Could not find Email or App Password in [CREDENTIALS] section")
        print(f"   Email found: {email}")
        print(f"   App Password found: {bool(app_password)}")
        sys.exit(1)

    return {
        'email': email,
        'app_password': app_password,
    }


def load_email_template():
    """Load HTML email template."""
    template_path = Path(__file__).parent / "coaching" / "emails" / "access-email-template.html"

    if not template_path.exists():
        print(f"❌ Email template not found: {template_path}")
        sys.exit(1)

    return template_path.read_text(encoding='utf-8')


def personalize_email(template, participant):
    """Replace placeholders in template with participant data."""
    html = template
    html = html.replace("{{PARTICIPANT_NAME}}", participant["name"])
    html = html.replace("{{PARTICIPANT_TOKEN}}", participant["token"])
    html = html.replace("{{PERSONAL_DASHBOARD_URL}}", participant["dashboard_url"])
    return html


def send_email(from_email, app_password, to_email, participant_name, html_body):
    """Send email via Gmail SMTP."""
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎯 Ton Espace Coaching Personnel — S10"
        msg['From'] = from_email
        msg['To'] = to_email

        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(html_part)

        print(f"📧 Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print(f"🔐 Authenticating as {from_email}...")
            server.login(from_email, app_password)

            print(f"📬 Sending email to {to_email} ({participant_name})...")
            server.send_message(msg)

        print(f"✅ Email sent successfully to {participant_name}!")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"❌ Authentication failed for {participant_name}. Check email and app password.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error for {participant_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error sending to {participant_name}: {e}")
        return False


def main():
    """Main function."""
    print("=" * 60)
    print("🎯 Envoi Emails d'Accès Coaching — Tous les Participants")
    print("=" * 60)

    # Load credentials
    print("\n📋 Chargement des credentials...")
    creds = load_credentials()
    print(f"✅ Credentials chargées: {creds['email']}")

    # Load email template
    print("\n📄 Chargement du template email...")
    template = load_email_template()
    print(f"✅ Template chargé ({len(template)} caractères)")

    # Email details
    from_email = creds['email']
    app_password = creds['app_password']

    # Confirm before sending
    print("\n" + "=" * 60)
    print(f"De: {from_email}")
    print(f"À: {len(PARTICIPANTS)} participants")
    print("Sujet: 🎯 Ton Espace Coaching Personnel — S10")
    print("=" * 60)
    print("\nParticipants:")
    for p in PARTICIPANTS:
        print(f"  • {p['name']} ({p['email']})")

    confirm = input("\n✓ Envoyer les emails? (oui/non): ").strip().lower()
    if confirm not in ['oui', 'o', 'yes', 'y']:
        print("❌ Envoi annulé.")
        sys.exit(0)

    # Send emails
    print("\n📧 Envoi en cours...\n")
    success_count = 0
    failed_count = 0

    for participant in PARTICIPANTS:
        print(f"\n--- {participant['name']} ---")

        personalized_html = personalize_email(template, participant)

        if send_email(
            from_email,
            app_password,
            participant['email'],
            participant['name'],
            personalized_html
        ):
            success_count += 1
        else:
            failed_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"✅ Envoyés avec succès: {success_count}/{len(PARTICIPANTS)}")
    if failed_count > 0:
        print(f"❌ Échecs: {failed_count}/{len(PARTICIPANTS)}")

    if success_count == len(PARTICIPANTS):
        print("\n" + "=" * 60)
        print("✅ TOUS LES EMAILS ENVOYÉS!")
        print("=" * 60)
        print("\n💡 Prochaines étapes:")
        print("  1. Tous les participants reçoivent leur email d'accès")
        print("  2. Ils cliquent sur le lien ou entrent leur clé manuellement")
        print("  3. Leur dashboard personnel se charge")
        print(f"\n📊 Dashboard Familial: https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("⚠️  CERTAINS EMAILS N'ONT PAS ÉTÉ ENVOYÉS")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
