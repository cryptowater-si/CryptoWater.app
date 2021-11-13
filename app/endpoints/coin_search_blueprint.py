from functools import wraps
from os import getenv

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_wtf import FlaskForm
from flask_csv import send_csv
from wtforms import StringField, validators, SubmitField, PasswordField

from lib.logger import log
from lib.address_validator import AddressValidator
from lib.chainz_cryptoid import CryptoID
from lib.csv_pickle import ValidateDownload, PickleThis


coin_search_blueprint = Blueprint("coin", __name__)


class SubmitAddressForm(FlaskForm):
    address = StringField("Address:", [validators.DataRequired()])
    submit = SubmitField("Check")


class AuthCsvDownloadForm(FlaskForm):
    username = StringField("Username:", [validators.DataRequired("Enter Username")])
    password = PasswordField("Password:", [validators.DataRequired("Enter Password")])
    submit = SubmitField("Download")


######################
def ip_lock_warp(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        ip = ValidateDownload.get_ip_addr(request)
        eip = getenv("CSV_IP_LOCK", None)
        # skip ip check if no ip is defined
        if not eip:
            return func(*args, **kwargs)
        elif eip and eip == ip:
            return func(*args, **kwargs)
        log.warning("Unauthorized ip: {0}".format(ip))
        abort(500, "c-c-c")
        return

    return wrapped


@coin_search_blueprint.route("/", methods=["GET", "POST"])
def scan_address():

    address_form = SubmitAddressForm()
    if address_form.validate_on_submit():
        address = AddressValidator.clean_address(address_form.address.data)
        a_status, a_msg = AddressValidator.validate_address(address)
        if not a_status:
            log.warning("Address validation failed: {0} - {1}".format(address, a_msg))
            flash("Invalid address", "warning")
            return redirect(url_for("coin.scan_address"))
        else:
            data = CryptoID().address_info(a_msg, address)
            if not data:
                log.warning("Error getting data from cryptoid")
                return redirect(url_for("coin.scan_address"))
            # save data to csv
            try:
                formatted_data = ValidateDownload.normalize_data(data, request)
                PickleThis.save_dict(formatted_data)
            except Exception as err:
                log.warning("Failed to save to csv... {0}".format(err))
            return render_template("coin/home.html", form=address_form, data=data)

    elif address_form.errors:
        log.warning("Form error: {0}".format(address_form.errors))
        return redirect(url_for("coin.scan_address"))
    return render_template("coin/home.html", form=address_form)


@coin_search_blueprint.route("/address/scan/get/csv", methods=["GET", "POST"])
@ip_lock_warp
def get_csv():
    form = AuthCsvDownloadForm()
    if form.validate_on_submit():
        if ValidateDownload.validate_un_pw(form.username.data, form.password.data):
            headers = ["scanTimeUTC", "coin", "address", "ip", "browser"]
            data = PickleThis.get_dict()
            return send_csv(data, "scanned_addresses.csv", headers)
        else:
            flash("Incorrect Username or Password", "danger")
            return redirect(url_for("coin.get_csv"))

    return render_template("coin/download.html", form=form)
