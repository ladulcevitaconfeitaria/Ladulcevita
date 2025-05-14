# -*- coding: utf-8 -*-
"""User-specific routes (dashboard, profile, etc.)."""

import sys
import os
# Ensure the application root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Import necessary models and db instance
from src.models.models import db, User, Purchase, DiscountRule # Import DiscountRule

user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="../templates/user")

@user_bp.route("/dashboard")
@login_required # Protect this route
def dashboard():
    """Renders the user's dashboard showing points, recent activity, etc."""
    user = current_user
    purchases = user.purchases.order_by(Purchase.purchase_date.desc()).limit(5).all()
    
    # Fetch available discounts based on user points and active rules
    available_discounts = DiscountRule.query.filter(
        DiscountRule.is_active == True,
        DiscountRule.points_required <= user.points
    ).order_by(DiscountRule.points_required).all()
    
    return render_template("dashboard.html", user=user, purchases=purchases, discounts=available_discounts)

@user_bp.route("/profile", methods=["GET", "POST"])
@login_required # Protect this route
def profile():
    """Allows user to view and update their profile information."""
    user = current_user
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        if not name or not email or not phone:
            flash("Nome, Email e WhatsApp são obrigatórios.", "warning")
            return redirect(url_for("user.profile"))

        if email != user.email and User.query.filter_by(email=email).first():
            flash("Este email já está em uso.", "warning")
            return redirect(url_for("user.profile"))
        if phone != user.phone and User.query.filter_by(phone=phone).first():
            flash("Este WhatsApp já está em uso.", "warning")
            return redirect(url_for("user.profile"))

        user.name = name
        user.email = email
        user.phone = phone

        if new_password:
            if not current_password or not check_password_hash(user.password_hash, current_password):
                flash("Senha atual incorreta.", "warning")
                return redirect(url_for("user.profile"))
            if new_password != confirm_new_password:
                flash("As novas senhas não coincidem.", "warning")
                return redirect(url_for("user.profile"))
            user.password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
            flash("Senha alterada com sucesso!", "success")

        try:
            db.session.commit()
            if not new_password:
                flash("Perfil atualizado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar perfil: {e}", "danger")

        return redirect(url_for("user.profile"))

    return render_template("profile.html", user=user)

@user_bp.route("/history")
@login_required # Protect this route
def history():
    """Shows the user's full purchase and points history."""
    user = current_user
    all_purchases = user.purchases.order_by(Purchase.purchase_date.desc()).all()
    # TODO: Create history.html template
    # return render_template("history.html", purchases=all_purchases, user=user)
    flash("Funcionalidade de histórico completo ainda em desenvolvimento.", "info")
    return redirect(url_for("user.dashboard"))

@user_bp.route("/redeem/<int:rule_id>", methods=["POST"])
@login_required
def redeem_discount(rule_id):
    """Handles the redemption of a discount by the user."""
    user = current_user
    rule = DiscountRule.query.filter_by(id=rule_id, is_active=True).first()

    if not rule:
        flash("Regra de desconto inválida ou inativa.", "warning")
        return redirect(url_for("user.dashboard"))

    if rule.points_required is None or user.points < rule.points_required:
        flash("Pontos insuficientes para resgatar este desconto.", "warning")
        return redirect(url_for("user.dashboard"))

    # Deduct points
    user.points -= rule.points_required

    # TODO: Implement actual discount application logic.
    # This might involve generating a coupon code, applying discount to next order,
    # logging the redemption, etc.
    # For now, just deduct points and flash a message.

    try:
        db.session.commit()
        flash(f"Desconto '{rule.name}' resgatado com sucesso! {rule.points_required} pontos foram deduzidos.", "success")
        # Log the redemption event if needed
    except Exception as e:
        db.session.rollback()
        user.points += rule.points_required # Rollback points deduction
        flash(f"Erro ao resgatar desconto: {e}", "danger")

    return redirect(url_for("user.dashboard"))

# Add other user-specific routes as needed

