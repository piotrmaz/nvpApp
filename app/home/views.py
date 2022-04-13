from flask import abort, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime

from . import home

from .forms import ConsumableForm, ConsumableConsumptionForm, ConsumableDeliveryForm, PackageReceiveForm, PackageDeliveryForm
from .. import db
from ..models import Consumable, ConsumableConsumption, ConsumableDelivery, Package, PackageSend, PackageReceive, PackageDelivery, Condition

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

def check_if_confirmed():
    """
    Prevent not confirmed from accessing the page
    """
    if not current_user.is_confirmed:
        abort(403)


@home.route('/consumables')
@login_required
def list_consumables():
    """
    List all consumables
    """

    check_if_confirmed()

    consumables = Consumable.query.all()
    return render_template('user/consumables/consumables.html',
                           consumables=consumables, title='Consumables')


@home.route('/consumables/consumption/<int:id>', methods=['GET', 'POST'])
@login_required
def consumption_consumables(id):
    """
    Consumption consumable
    """

    check_if_confirmed()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    consumption = consumable.quantity
    form = ConsumableConsumptionForm(obj=consumable)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('home.list_consumables'))

    if form.validate_on_submit():

        now = datetime.now()
        curr_user = current_user.id


        consum_consumptions = ConsumableConsumption()

        consum_consumptions.consumab_id=consumable.id
        consum_consumptions.user_consumption_id=curr_user
        consum_consumptions.date=now
        consum_consumptions.quantity=request.form['quantity']

        db.session.add(consum_consumptions)

        curr_consum = consum_consumptions.quantity
        subtraction = int(consumption) - int(curr_consum)
        consumable.quantity = subtraction

        db.session.commit()
        flash('You have successfully edited the consumable.')

        # redirect to the consumables page
        return redirect(url_for('home.list_consumables'))

    return render_template('user/consumables/consumable.html', action="Edit",
                           add_consumable=add_consumable, form=form,
                           consumable=consumable, title="Consumables consumption")

@home.route('/consumable/details/<int:id>', methods=['GET', 'POST'])
@login_required
def details_consumable(id):
    "Details one consumable"

    check_if_confirmed()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    consumption = db.session.query(ConsumableConsumption).filter(ConsumableConsumption.consumab_id==consumable.id).order_by(ConsumableConsumption.date.desc()).all()
    delivers = db.session.query(ConsumableDelivery).filter(ConsumableDelivery.consumable_id==consumable.id).order_by(ConsumableDelivery.date.desc()).all()

    return render_template('admin/consumable_details/consumable_details.html',
                        consumable=consumable, consumption=consumption, delivers=delivers, title='Details consumable')


@home.route('/consumables/delivery/<int:id>', methods=['GET', 'POST'])
@login_required
def delivery_consumables(id):
    """
    Delivery consumable
    """

    check_if_confirmed()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    delivery = consumable.quantity
    form = ConsumableDeliveryForm(obj=consumable)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('home.list_consumables'))

    if form.validate_on_submit():

        now = datetime.now()
        curr_user = current_user.id
        suppliery = form['supplier_id'].data

        consum_delivery = ConsumableDelivery()

        consum_delivery.consumable_id=consumable.id
        consum_delivery.user_delivery_id=curr_user
        consum_delivery.supplier_consumable_delivery_id=suppliery.id
        consum_delivery.quantity=request.form['quantity'],
        consum_delivery.date=now

        db.session.add(consum_delivery)

        curr_consum = request.form['quantity']
        addd = int(curr_consum) + int(delivery)
        consumable.quantity = addd

        db.session.commit()
        flash('You have successfully edited the consumable.')
        # redirect to the consumables page
        return redirect(url_for('home.list_consumables'))

    return render_template('user/consumables/consumable.html', action="Edit",
                           add_consumable=add_consumable, form=form,
                           consumable=consumable, title="Consumables delivery")


# package view

@home.route('/packages')
@login_required
def list_packages():
    """
    List all packages
    """
    check_if_confirmed()

    packages = Package.query.order_by(Package.description.asc()).all()
    return render_template('user/packages/packages.html',
                           packages=packages, title='Packages')

@home.route('/packages/delivery/<int:id>', methods=['GET', 'POST'])
@login_required
def delivery_packages(id):
    """
    Delivery packages for users
    """
    check_if_confirmed()

    add_package = False

    package = Package.query.get_or_404(id)
    delivery = package.quantity

    form = PackageDeliveryForm(obj=package)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('home.list_packages'))

    if form.validate_on_submit():

        now = datetime.now()
        curr_user = current_user.id
        suppliery = form['supplier_id'].data

        package_delivery = PackageDelivery()

        package_delivery.package_id=package.id,
        package_delivery.quantity=request.form['quantity'],
        package_delivery.description=form.description.data,
        package_delivery.supplier_id=suppliery.id,
        package_delivery.user_id=curr_user
        package_delivery.date=now

        db.session.add(package_delivery)

        curr_inside = package.inside
        curr_package = request.form['quantity']
        addd = int(curr_package) + int(delivery)

        package.inside = int(curr_package) + int(curr_inside)
        package.quantity = addd


        db.session.commit()
        flash('You have successfully registered the delivery.')
        # redirect to the packages page
        return redirect(url_for('home.list_packages'))

    return render_template('user/packages/package.html', action="Edit",
                           add_package=add_package, form=form,
                           package=package, title="Delivery Package")


@home.route('/packages/send/<int:id>', methods=['GET', 'POST'])
@login_required
def send_packages(id):
    """
    Send packages for users
    """
    check_if_confirmed()

    add_package = False

    package = Package.query.get_or_404(id)

    form = PackageDeliveryForm(obj=package)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('home.list_packages'))

    if form.validate_on_submit():

        now = datetime.now()
        curr_user = current_user.id
        suppliery = form['supplier_id'].data

        package_send = PackageSend()

        package_send.package_id=package.id,
        package_send.quantity=request.form['quantity'],
        package_send.description=form.description.data,
        package_send.supplier_id=suppliery.id,
        package_send.user_id=curr_user
        package_send.date=now

        db.session.add(package_send)

        curr_inside = package.inside
        curr_package = request.form['quantity']

        package.inside = curr_inside - int(curr_package)
        package.outside += int(curr_package)


        db.session.commit()
        flash('You have successfully send package.')
        # redirect to the packages page
        return redirect(url_for('home.list_packages'))

    return render_template('user/packages/package.html', action="Edit",
                           add_package=add_package, form=form,
                           package=package, title="Send Package")

# receive package
@home.route('/packages/receive/<int:id>', methods=['GET', 'POST'])
@login_required
def receive_packages(id):
    """
    Receive packages for users
    """
    check_if_confirmed()

    add_package = False

    package = Package.query.get_or_404(id)
    condition = Condition.query.all()

    form = PackageReceiveForm(obj=package)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('home.list_packages'))

    if form.validate_on_submit():

        now = datetime.now()
        curr_user = current_user.id
        suppliery = form['supplier'].data

        package_receive = PackageReceive()

        package_receive.package_id=package.id,
        package_receive.condition=request.form['condition'],
        package_receive.quantity=request.form['quantity'],
        package_receive.description=form.description.data,
        package_receive.supplier=suppliery.id,
        package_receive.user_id=curr_user,
        package_receive.date=now

        db.session.add(package_receive)

        curr_inside = package.inside
        curr_outside = package.outside
        curr_package = request.form['quantity']

        req = request.form.get("condition")
        condit = db.session.query(Condition).filter(Condition.name=="OK").first()
        curr_condition = condit.id

        if req != str(curr_condition):
            package.quantity -= int(curr_package)
            package.outside = curr_outside - int(curr_package)
        else:
            package.inside += int(curr_package)
            package.outside = curr_outside - int(curr_package)

        db.session.commit()

        flash('You have successfully received package.')
        # redirect to the pac/kages page
        return redirect(url_for('home.list_packages'))

    return render_template('user/packages/package.html', action="Add",
                           add_package=add_package, form=form,
                           package=package, title="Receive Package")

@home.route('/packages/packages_details/packages_details/<int:id>', methods=['GET', 'POST'])
@login_required
def details_packages(id):
    "Details one package"

    check_if_confirmed()

    add_package = False

    package = Package.query.get_or_404(id)
    # consumption = db.session.query(ConsumableConsumption).filter(ConsumableConsumption.consumab_id==consumable.id).order_by(ConsumableConsumption.date.desc()).all()
    delivers = db.session.query(PackageDelivery).filter(PackageDelivery.package_id==package.id).order_by(PackageDelivery.date.desc()).all()

    return render_template('user/packages/packages_details/packages_details.html',
                        package=package, delivers=delivers, title='Details package')
