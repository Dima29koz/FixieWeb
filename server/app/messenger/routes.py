from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import messenger
from ...utils.role_required import allowed_roles

# Predefined rooms for chat
ROOMS = ["lounge", "news", "games", "coding"]


@messenger.route("/chat", methods=['GET', 'POST'])
@login_required
@allowed_roles(roles={'Admin', 'Member'})
def chat():
    # return render_template("chat.html", username=current_user.user_name, rooms=current_user.chats)
    return render_template("chat.html", username=current_user.user_name, rooms=ROOMS)
