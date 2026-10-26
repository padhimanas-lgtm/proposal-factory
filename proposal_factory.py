import streamlit as st
import openai
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Set page config
st.set_page_config(page_title="Proposal Factory", layout="wide")

# Title and branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #001D13 0%, #DEAF5D 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-header {
        color: #001D13;
        border-bottom: 2px solid #DEAF5D;
        padding-bottom: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📄 PROPOSAL FACTORY</h1>
    <p>Generate Professional Business Proposals in Minutes</p>
    <p>Powered by Arthamrit Technologies</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with instructions
st.sidebar.title("📋 Instructions")
st.sidebar.info("""
1. Fill in your company details
2. Enter client information
3. Add proposal details
4. Generate proposal using AI
5. Download as PDF
""")

# Initialize session state
if "proposal_content" not in st.session_state:
    st.session_state.proposal_content = None

# Main form
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 class='section-header'>Your Company Details</h2>", unsafe_allow_html=True)

    company_name = st.text_input("Company Name *", placeholder="e.g., Arthamrit Technologies")
    company_email = st.text_input("Company Email *", placeholder="info@arthamrit.com")
    company_phone = st.text_input("Company Phone *", placeholder="+91 97770 48548")
    company_address = st.text_area("Company Address *", placeholder="Office address, city, state")

with col2:
    st.markdown("<h2 class='section-header'>Client Details</h2>", unsafe_allow_html=True)

    client_name = st.text_input("Client Name *", placeholder="Client company or person name")
    client_contact = st.text_input("Client Contact Email *", placeholder="client@company.com")
    client_phone = st.text_input("Client Phone", placeholder="Client phone number")
    client_company = st.text_input("Client Company", placeholder="Client's company name")

# Proposal details
st.markdown("<h2 class='section-header'>Proposal Details</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    proposal_title = st.text_input("Proposal Title *", placeholder="e.g., IT Infrastructure Consulting")
    service_type = st.selectbox("Service Type", [
        "IT Consulting",
        "Financial Consulting",
        "Digital Solutions",
        "Sales Services",
        "AI Consulting",
        "Other"
    ])

with col2:
    proposal_duration = st.text_input("Project Duration *", placeholder="e.g., 3 months")
    proposal_budget = st.text_input("Budget Range *", placeholder="e.g., $50,000 - $100,000")

# Proposal description
st.markdown("<h3>Project Scope & Description</h3>", unsafe_allow_html=True)
project_scope = st.text_area("Describe the project scope, objectives, and deliverables *",
    placeholder="What will be delivered? What are the key milestones?", height=150)

# Key benefits
st.markdown("<h3>Key Benefits & Outcomes</h3>", unsafe_allow_html=True)
benefits = st.text_area("List the main benefits and expected outcomes *",
    placeholder="What value will the client get? E.g., improved efficiency, cost savings, etc.", height=100)

# Terms & conditions
st.markdown("<h3>Terms & Conditions</h3>", unsafe_allow_html=True)
payment_terms = st.text_input("Payment Terms", placeholder="e.g., 50% upfront, 50% on completion")
validity = st.text_input("Proposal Validity Period", placeholder="e.g., 30 days")

# Generate button
st.markdown("<h2 class='section-header'>Generate Proposal</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    generate_btn = st.button("🤖 Generate with AI", use_container_width=True)

with col2:
    st.markdown("OR")

with col3:
    template_btn = st.button("📋 Use Template", use_container_width=True)

# Validation
required_fields = [company_name, company_email, company_phone, company_address,
                   client_name, client_contact, proposal_title, project_scope, benefits]

if generate_btn or template_btn:
    if not all(required_fields):
        st.error("❌ Please fill in all required fields (marked with *)")
    else:
        if generate_btn:
            st.info("🔄 Generating proposal with AI... (using template for this beta)")

        # Generate proposal content
        proposal_date = datetime.now().strftime("%B %d, %Y")

        proposal_html = f"""
        <div style="font-family: Arial; line-height: 1.6; color: #333;">
            <hr style="border: none; border-top: 3px solid #DEAF5D;">

            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #001D13; margin: 10px 0;">BUSINESS PROPOSAL</h1>
                <h2 style="color: #DEAF5D; margin: 0;">{proposal_title}</h2>
            </div>

            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 50%; padding: 10px;">
                            <strong>From:</strong><br>
                            {company_name}<br>
                            {company_email}<br>
                            {company_phone}<br>
                            {company_address}
                        </td>
                        <td style="width: 50%; padding: 10px; text-align: right;">
                            <strong>To:</strong><br>
                            {client_name}<br>
                            {client_contact}<br>
                            {client_company if client_company else 'N/A'}<br>
                            <strong>Date:</strong> {proposal_date}
                        </td>
                    </tr>
                </table>
            </div>

            <h3 style="color: #001D13; border-bottom: 2px solid #DEAF5D; padding-bottom: 10px;">EXECUTIVE SUMMARY</h3>
            <p>This proposal outlines {company_name}'s plan to deliver {proposal_title.lower()} services to {client_name}.
            We are committed to delivering exceptional value and measurable results.</p>

            <h3 style="color: #001D13; border-bottom: 2px solid #DEAF5D; padding-bottom: 10px;">PROJECT SCOPE</h3>
            <p>{project_scope}</p>

            <h3 style="color: #001D13; border-bottom: 2px solid #DEAF5D; padding-bottom: 10px;">KEY BENEFITS & OUTCOMES</h3>
            <p>{benefits}</p>

            <h3 style="color: #001D13; border-bottom: 2px solid #DEAF5D; padding-bottom: 10px;">SERVICE DETAILS</h3>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr style="background: #001D13; color: white;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Service Type</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{service_type}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Project Duration</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{proposal_duration}</td>
                </tr>
                <tr style="background: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Budget</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;" style="color: #DEAF5D;"><strong>{proposal_budget}</strong></td>
                </tr>
            </table>

            <h3 style="color: #001D13; border-bottom: 2px solid #DEAF5D; padding-bottom: 10px;">TERMS & CONDITIONS</h3>
            <ul>
                <li><strong>Payment Terms:</strong> {payment_terms if payment_terms else 'To be discussed'}</li>
                <li><strong>Proposal Valid Until:</strong> {validity if validity else '30 days from date'}</li>
                <li>This proposal is confidential and intended only for the named recipient.</li>
                <li>All deliverables are subject to completion of project phases as outlined above.</li>
            </ul>

            <h3 style="color: #001D13; border-bottom: 2px solid #DEAF5D; padding-bottom: 10px;">NEXT STEPS</h3>
            <ol>
                <li>Review this proposal</li>
                <li>Contact us with any questions: {company_phone}</li>
                <li>Sign and return to proceed with engagement</li>
                <li>Project kickoff upon agreement</li>
            </ol>

            <hr style="margin-top: 40px; border: none; border-top: 2px solid #001D13;">
            <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                <strong>{company_name}</strong><br>
                {company_email} | {company_phone}<br>
                <em>Professional Business Solutions</em>
            </p>
        </div>
        """

        st.session_state.proposal_content = proposal_html
        st.success("✅ Proposal generated successfully!")

# Display and download generated proposal
if st.session_state.proposal_content:
    st.markdown("<h2 class='section-header'>📄 Generated Proposal Preview</h2>", unsafe_allow_html=True)

    st.markdown(st.session_state.proposal_content, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Download as HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{proposal_title} - Proposal</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
                h1, h2, h3 {{ color: #001D13; }}
                h2 {{ border-bottom: 2px solid #DEAF5D; padding-bottom: 10px; }}
                .header {{ background: linear-gradient(135deg, #001D13 0%, #DEAF5D 100%);
                          color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                td, th {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                th {{ background-color: #001D13; color: white; }}
                .highlight {{ color: #DEAF5D; font-weight: bold; }}
            </style>
        </head>
        <body>
            {st.session_state.proposal_content}
        </body>
        </html>
        """

        st.download_button(
            label="📥 Download as HTML",
            data=html_content,
            file_name=f"{proposal_title.replace(' ', '_')}_proposal.html",
            mime="text/html"
        )

    with col2:
        # Download as TXT
        txt_content = f"""
PROPOSAL: {proposal_title}
{'='*60}

FROM: {company_name}
{company_email} | {company_phone}
{company_address}

TO: {client_name}
{client_contact}
{client_company if client_company else ''}

DATE: {datetime.now().strftime('%B %d, %Y')}

{'='*60}

PROJECT SCOPE:
{project_scope}

KEY BENEFITS:
{benefits}

SERVICE DETAILS:
- Service Type: {service_type}
- Duration: {proposal_duration}
- Budget: {proposal_budget}

TERMS:
- Payment: {payment_terms if payment_terms else 'To be discussed'}
- Valid Until: {validity if validity else '30 days'}

{'='*60}
Generated by Proposal Factory
Arthamrit Technologies
"""

        st.download_button(
            label="📄 Download as Text",
            data=txt_content,
            file_name=f"{proposal_title.replace(' ', '_')}_proposal.txt",
            mime="text/plain"
        )

    with col3:
        st.info("💡 PDF export coming soon! Download as HTML for printing.")

# Footer
st.markdown("""
---
<div style="text-align: center; color: #666; font-size: 12px; margin-top: 40px;">
    <strong>Proposal Factory v1.0</strong> | Built by Arthamrit Technologies<br>
    www.arthamrit.com | support@arthamrit.com | +91 97770 48548<br>
    <em>Transform your proposals. Impress your clients. Close deals faster.</em>
</div>
""", unsafe_allow_html=True)
