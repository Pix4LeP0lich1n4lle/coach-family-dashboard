#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to send Joseph's personalized coaching space onboarding email.
Uses SMTP credentials from .connexion file.
"""

import smtplib
import sys
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

def load_credentials():
    """Load SMTP credentials from .connexion file."""
    # Path: /home/chakra/ai-lab/PROJECTS/Coach_Suivies/.credentials/.connexion
    cred_path = Path(__file__).parent.parent.parent.parent / ".credentials" / ".connexion"

    if not cred_path.exists():
        print(f"❌ Credentials file not found: {cred_path}")
        sys.exit(1)

    # Read file directly - grab ONLY from [CREDENTIALS] section
    content = cred_path.read_text()
    lines = content.split('\n')

    email = None
    app_password = None
    in_credentials_section = False

    for line in lines:
        line = line.strip()

        # Check if we're entering CREDENTIALS section
        if line == '[CREDENTIALS]':
            in_credentials_section = True
            continue

        # Stop reading when we hit another section
        if line.startswith('[') and line != '[CREDENTIALS]':
            in_credentials_section = False
            continue

        # Only parse lines in CREDENTIALS section
        if in_credentials_section:
            if line.startswith('Email='):
                email = line.split('=', 1)[1].strip()
            elif line.startswith('App Password='):
                app_password = line.split('=', 1)[1].strip()

    if not email or not app_password:
        print("❌ Could not find Email or App Password in [CREDENTIALS] section")
        sys.exit(1)

    return {
        'email': email,
        'app_password': app_password,
    }

def load_email_template():
    """Load HTML email template."""
    template_path = Path(__file__).parent / "email-joseph-onboarding.html"

    if not template_path.exists():
        print(f"❌ Email template not found: {template_path}")
        sys.exit(1)

    return template_path.read_text(encoding='utf-8')

def send_email(from_email, app_password, to_email, subject, html_body):
    """Send email via Gmail SMTP."""
    try:
        # Gmail SMTP settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Attach HTML content
        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(html_part)

        # Connect and send
        print(f"📧 Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print(f"🔐 Authenticating as {from_email}...")
            server.login(from_email, app_password)

            print(f"📬 Sending email to {to_email}...")
            server.send_message(msg)

        print(f"✅ Email sent successfully to {to_email}!")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check email and app password.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("🎯 Envoi Email Coaching - Joseph Delorey")
    print("=" * 60)

    # Load credentials
    print("\n📋 Chargement des credentials...")
    creds = load_credentials()
    print(f"✅ Credentials chargées: {creds['email']}")

    # Load email template
    print("\n📄 Chargement du template email...")
    html_body = load_email_template()
    print(f"✅ Template chargé ({len(html_body)} caractères)")

    # Email details
    from_email = creds['email']
    app_password = creds['app_password']
    to_email = "jdelorey02@proton.me"
    subject = "🎯 Ton Espace Coaching Personnel — S10"

    # Confirm before sending
    print("\n" + "=" * 60)
    print(f"De: {from_email}")
    print(f"À: {to_email}")
    print(f"Sujet: {subject}")
    print("=" * 60)

    confirm = input("\n✓ Envoyer cet email? (oui/non): ").strip().lower()
    if confirm not in ['oui', 'o', 'yes', 'y']:
        print("❌ Envoi annulé.")
        sys.exit(0)

    # Send email
    print("\n📧 Envoi en cours...")
    if send_email(from_email, app_password, to_email, subject, html_body):
        print("\n" + "=" * 60)
        print("✅ SUCCÈS! Email envoyé à Joseph")
        print("=" * 60)
        print("\n💡 Prochaines étapes:")
        print("  1. Joseph reçoit l'email avec le lien d'accès")
        print("  2. Il clique sur le lien ou entre manuellement sa clé")
        print("  3. Son dashboard personnel se charge")
        print("\n📊 Lien: https://pix4lep0lich1n4lle.github.io/coach-family-dashboard/coaching/")
        print("🔑 Clé: joseph_coach_secret_x7k2m9n")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ ERREUR: Email non envoyé")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
