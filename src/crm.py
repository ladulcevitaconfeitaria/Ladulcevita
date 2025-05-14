# -*- coding: utf-8 -*-
"""CRM/Admin routes (customer management, segmentation, messaging)."""

import sys
import os
import json # For simulating API call payload
# Ensure the application root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Blueprint, render_template, request, redirect, url_for, flash
# Import necessary models and functions
from src.models.models import db, User, Segment, DiscountRule, Purchase # Import DiscountRule and Purchase
from flask_login import login_required # Assuming admin login is required
from datetime import datetime # For purchase date

# TODO: Implement proper admin authentication/authorization
# For now, we assume routes are protected, but the decorator is commented out

crm_bp = Blueprint("crm", __name__, url_prefix="/admin/crm", template_folder="../templates/crm")

# --- Helper Function for WhatsApp Simulation ---
def simulate_whatsapp_send(phone_number, message):
    """Simulates sending a WhatsApp message via an API.
    
    IMPORTANT COMPLIANCE NOTES (Based on WhatsApp Business Policy):
    1. OPT-IN REQUIRED: Ensure users have explicitly agreed (opted-in) to receive messages 
       from your business on WhatsApp before sending any messages.
    2. MESSAGE TEMPLATES: For business-initiated messages outside the 24-hour customer service window,
       you MUST use pre-approved Message Templates. The free-form text simulation here is only 
       valid within the 24-hour window or requires template approval.
    3. API INTEGRATION: This is a simulation. Real integration requires using the Meta Cloud API 
       or a Business Solution Provider (BSP), handling API keys, and adhering to their specific format.
    4. AVOID SPAM: Do not send unsolicited messages. Ensure messages are relevant and expected.
    5. RESPECT OPT-OUTS: Implement a clear way for users to stop receiving messages.
    """
    # In a real application, this would interact with a WhatsApp Business API provider
    # (e.g., Twilio, Meta API directly, etc.) using requests library or their SDK.
    print(f"--- SIMULATING WHATSAPP SEND ---")
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print(f"Compliance Notes: Opt-in assumed, Template potentially required.")
    # Example of what a real API call might look like (conceptual)
    # api_endpoint = "https://api.provider.com/v1/messages"
    # headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}
    # payload = {
    #     "to": phone_number, # Ensure format matches API requirements (e.g., +55119...)
    #     "type": "template", # Use 'template' for business-initiated messages
    #     "template": {
    #         "name": "your_approved_template_name",
    #         "language": { "code": "pt_BR" },
    #         "components": [ ... ] # Variables for the template
    #      }
    #     # Or use "text" type within 24h window:
    #     # "type": "text",
    #     # "text": {"body": message}
    # }
    # try:
    #     response = requests.post(api_endpoint, headers=headers, json=payload)
    #     response.raise_for_status() # Raise an exception for bad status codes
    #     print(f"Message sent successfully to {phone_number}")
    #     return True
    # except requests.exceptions.RequestException as e:
    #     print(f"Error sending message to {phone_number}: {e}")
    #     return False
    print(f"--- END SIMULATION ---")
    return True # Assume success for simulation
# ---------------------------------------------

@crm_bp.route("/dashboard")
# @login_required
def dashboard():
    """Renders the CRM dashboard."""
    total_users = User.query.count()
    total_segments = Segment.query.count()
    total_rules = DiscountRule.query.count()
    return render_template("crm_dashboard.html", total_users=total_users, total_segments=total_segments, total_rules=total_rules)

@crm_bp.route("/users")
# @login_required
def list_users():
    """Lists all registered users with search/filter options."""
    users = User.query.order_by(User.registration_date.desc()).all()
    segments = Segment.query.order_by(Segment.name).all() # For assignment dropdown
    return render_template("crm_users.html", users=users, segments=segments)

@crm_bp.route("/users/<int:user_id>/assign_segment", methods=["POST"])
# @login_required
def assign_user_segment(user_id):
    """Assigns a user to a specific segment."""
    user = User.query.get_or_404(user_id)
    segment_id = request.form.get("segment_id")

    if segment_id == "None" or not segment_id:
        user.segment_id = None
        flash(f"Usuário {user.name} removido de qualquer segmento.", "info")
    else:
        segment = Segment.query.get(segment_id)
        if segment:
            user.segment_id = segment.id
            flash(f"Usuário {user.name} atribuído ao segmento ", "success")
        else:
            flash("Segmento inválido.", "warning")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao atribuir segmento: {e}", "danger")

    return redirect(url_for("crm.list_users"))

@crm_bp.route("/segments", methods=["GET", "POST"])
# @login_required
def manage_segments():
    """Manages customer segments (creation, viewing, deletion)."""
    if request.method == "POST":
        action = request.form.get("action")
        segment_id = request.form.get("segment_id")

        if action == "create":
            name = request.form.get("name")
            description = request.form.get("description")
            if name and not Segment.query.filter_by(name=name).first():
                new_segment = Segment(name=name, description=description)
                db.session.add(new_segment)
                try:
                    db.session.commit()
                    flash(f"Segmento ", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Erro ao criar segmento: {e}", "danger")
            elif not name:
                 flash("Nome do segmento é obrigatório.", "warning")
            else:
                flash("Segmento com este nome já existe.", "warning")
        
        elif action == "delete" and segment_id:
             segment = Segment.query.get(segment_id)
             if segment:
                 User.query.filter_by(segment_id=segment_id).update({User.segment_id: None})
                 db.session.delete(segment)
                 try:
                     db.session.commit()
                     flash(f"Segmento ", "success")
                 except Exception as e:
                     db.session.rollback()
                     flash(f"Erro ao deletar segmento: {e}", "danger")
             else:
                 flash("Segmento não encontrado.", "warning")

        return redirect(url_for("crm.manage_segments"))

    segments = Segment.query.order_by(Segment.name).all()
    return render_template("crm_segments.html", segments=segments)

@crm_bp.route("/discounts", methods=["GET", "POST"])
# @login_required
def manage_discounts():
    """Manages discount rules (creation, viewing, deletion)."""
    if request.method == "POST":
        action = request.form.get("action")
        rule_id = request.form.get("rule_id")

        if action == "create":
            name = request.form.get("name")
            description = request.form.get("description")
            points_required = request.form.get("points_required", type=int)
            discount_type = request.form.get("discount_type")
            discount_value = request.form.get("discount_value", type=float)
            is_active = "is_active" in request.form

            if not name or not discount_type or discount_value is None:
                flash("Nome, Tipo e Valor do Desconto são obrigatórios.", "warning")
            else:
                new_rule = DiscountRule(
                    name=name, 
                    description=description, 
                    points_required=points_required, 
                    discount_type=discount_type, 
                    discount_value=discount_value, 
                    is_active=is_active
                )
                db.session.add(new_rule)
                try:
                    db.session.commit()
                    flash(f"Regra de desconto ", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Erro ao criar regra: {e}", "danger")
        
        elif action == "delete" and rule_id:
            rule = DiscountRule.query.get(rule_id)
            if rule:
                db.session.delete(rule)
                try:
                    db.session.commit()
                    flash(f"Regra de desconto ", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Erro ao deletar regra: {e}", "danger")
            else:
                flash("Regra não encontrada.", "warning")
        
        elif action == "toggle_active" and rule_id:
            rule = DiscountRule.query.get(rule_id)
            if rule:
                rule.is_active = not rule.is_active
                try:
                    db.session.commit()
                    status = "ativada" if rule.is_active else "desativada"
                    flash(f"Regra ", "info")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Erro ao alterar status da regra: {e}", "danger")
            else:
                flash("Regra não encontrada.", "warning")

        return redirect(url_for("crm.manage_discounts"))

    rules = DiscountRule.query.order_by(DiscountRule.points_required).all()
    return render_template("crm_discounts.html", rules=rules)

@crm_bp.route("/add_purchase", methods=["POST"])
# @login_required
def add_purchase():
    """Adds a purchase record for a user and awards points."""
    user_id = request.form.get("user_id", type=int)
    amount = request.form.get("amount", type=float)
    user = User.query.get(user_id)

    if not user or amount is None or amount <= 0:
        flash("Usuário inválido ou valor da compra inválido.", "warning")
        return redirect(url_for("crm.list_users"))

    points_earned = int(amount)
    new_purchase = Purchase(
        user_id=user.id,
        amount=amount,
        points_earned=points_earned,
        purchase_date=datetime.utcnow()
    )
    user.points = (user.points or 0) + points_earned

    try:
        db.session.add(new_purchase)
        db.session.commit()
        flash(f"Compra de R$ {amount:.2f} registrada para {user.name}. Pontos ganhos: {points_earned}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao registrar compra: {e}", "danger")

    return redirect(url_for("crm.list_users"))


@crm_bp.route("/messaging", methods=["GET", "POST"])
# @login_required
def send_message():
    """Sends messages (e.g., WhatsApp) to selected segments via simulation."""
    if request.method == "POST":
        segment_id = request.form.get("segment_id")
        message = request.form.get("message")

        if not segment_id or not message:
            flash("Selecione um segmento e digite a mensagem.", "warning")
            return redirect(url_for("crm.send_message"))

        segment = Segment.query.get(segment_id)
        if not segment:
            flash("Segmento inválido.", "warning")
            return redirect(url_for("crm.send_message"))

        users_in_segment = User.query.filter_by(segment_id=segment.id).all()
        if not users_in_segment:
            flash(f"Nenhum usuário encontrado no segmento ", "info")
            return redirect(url_for("crm.send_message"))

        success_count = 0
        fail_count = 0
        print(f"\n--- STARTING WHATSAPP SIMULATION FOR SEGMENT: {segment.name} ---")
        for user in users_in_segment:
            if user.phone:
                formatted_phone = user.phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if not formatted_phone.startswith("+"):
                     if len(formatted_phone) >= 10:
                         formatted_phone = "+55" + formatted_phone
                     else:
                         print(f"Skipping user {user.name} ({user.id}): Invalid phone format {user.phone}")
                         fail_count += 1
                         continue
                
                if simulate_whatsapp_send(formatted_phone, message):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                print(f"Skipping user {user.name} ({user.id}): No phone number.")
                fail_count += 1
        print(f"--- WHATSAPP SIMULATION COMPLETE FOR SEGMENT: {segment.name} ---")
        print(f"Success: {success_count}, Failed/Skipped: {fail_count}\n")

        flash(f"Simulação de envio para o segmento ", "success")
        flash(f"Sucesso: {success_count}, Falhas/Ignorados: {fail_count}. Verifique o console para detalhes.", "info")
        
        # TODO: Log this action in the database if needed

        return redirect(url_for("crm.send_message"))

    # GET request
    segments = Segment.query.all()
    return render_template("crm_messaging.html", segments=segments)

# Add other CRM/admin routes as needed
