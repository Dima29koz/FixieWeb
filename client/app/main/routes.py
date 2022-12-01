from flask import render_template, redirect, url_for

from . import main
from .forms import IncidentForm
from ...utils.data_loader import send_incident


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/incidents', methods=["POST", "GET"])
def incidents():
    form = IncidentForm()
    if form.validate_on_submit():
        send_incident(form.name.data,
                      form.email.data,
                      form.subject.data,
                      form.description.data)
        return redirect(url_for('main.incident_send_success'))

    return render_template('incidents.html', form=form)


@main.route('/incidents/success')
def incident_send_success():
    return render_template('incident_send_success.html')
