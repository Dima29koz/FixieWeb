from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import messenger

# Predefined rooms for chat
ROOMS = ["lounge", "news", "games", "coding"]


@messenger.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    return render_template("chat.html", username=current_user.user_name, rooms=ROOMS)
