# -*- coding: utf-8 -*-
"""Authentication routes.

Handles user login, registration, and logout.
"""

import sys
import os
# Ensure the application root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash # Needed for registration

# Assuming models.py is in the same directory (src)
from .models import db, User

auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static", url_prefix="/auth") # Added url_prefix

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard")) # Redirect if already logged in

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            flash("Email ou senha inválidos. Por favor, tente novamente.")
            return redirect(url_for("auth.login")) # Redirect back to login page

        # Log the user in
        login_user(user, remember=remember)
        flash("Login realizado com sucesso!")
        # Redirect to the dashboard (assuming it exists in main blueprint)
        # Check if next parameter exists for redirect after login
        next_page = request.args.get("next")
        if next_page:
             return redirect(next_page)
        else:
             return redirect(url_for("main.dashboard"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handles user registration."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard")) # Redirect if already logged in

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Basic validation
        if not email or not name or not phone or not password or not confirm_password:
            flash("Todos os campos são obrigatórios.")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("As senhas não coincidem.")
            return redirect(url_for("auth.register"))

        # Check if user already exists
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_phone = User.query.filter_by(phone=phone).first()
        if existing_user_email:
            flash("Este email já está registado.")
            return redirect(url_for("auth.register"))
        if existing_user_phone:
            flash("Este telefone já está registado.")
            return redirect(url_for("auth.register"))

        # Create new user
        new_user = User(email=email, name=name, phone=phone)
        new_user.set_password(password) # Hash the password

        # Add user to database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registo realizado com sucesso! Faça o login.")
            # Log the user in automatically after registration
            # login_user(new_user)
            # return redirect(url_for("main.dashboard"))
            return redirect(url_for("auth.login")) # Redirect to login after successful registration
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao registar utilizador: {e}")
            return redirect(url_for("auth.register"))

    return render_template("register.html")

@auth_bp.route("/logout")
@login_required # Ensure user is logged in to logout
def logout():
    """Handles user logout."""
    logout_user()
    flash("Logout realizado com sucesso.")
    return redirect(url_for("main.index")) # Redirect to the main index page
