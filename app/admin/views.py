from flask import abort, flash, redirect, render_template, url_for, request, session
from flask_login import current_user, login_required
from sqlalchemy.orm import join
from datetime import datetime

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm, SupplierForm, UnitsForm, ConsumableForm, ParcelForm, ConsumableConsumptionForm, ConsumableDeliveryForm, ConditionForm, DirectionForm, PackageForm, PackageDeliveryForm, PackageFormEdit, PackageReceiveForm
from .. import db
from ..models import Department, Role, Employee, Supplier, Unit, Consumable, Parcel, ConsumableConsumption, ConsumableDelivery, Condition, Direction, Package, PackageDelivery, PackageSend, PackageReceive


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_departments'))
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.cancel.data:
        return redirect(url_for('admin.list_departments'))
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_roles'))
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.cancel.data:
        return redirect(url_for('admin.list_roles'))
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

    # Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.cancel.data:
        return redirect(url_for('admin.list_employees'))

    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the employee page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

@admin.route('/employees/confirmed/<int:id>', methods=['GET', 'POST'])
@login_required
def confirmed_employee(id):
    """
    Confirmed new employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    employee.is_confirmed = True

    db.session.commit()
    flash('You have successfully confirmed new employee.')

    return redirect(url_for('admin.list_employees'))

@admin.route('/employee/priviliges/<int:id>', methods=['GET', 'POST'])
@login_required
def grant_admin_priviliges(id):
    """
    Grant admin priviliges for employee
    """

    check_admin()

    employee = Employee.query.get_or_404(id)
    employee.is_admin = True
    employee.is_granted = True

    db.session.commit()
    flash('You have successfully granted admin priviliges for employee.')
    return redirect(url_for('admin.list_employees'))


@admin.route('/employee/deny/<int:id>', methods=['GET', 'POST'])
@login_required
def deny_admin_priviliges(id):
    """
    Deny admin priviliges for employee
    """

    check_admin()

    employee = Employee.query.get_or_404(id)
    employee.is_admin = False
    employee.is_granted = False

    db.session.commit()
    flash('You have successfully deny admin priviliges for employee.')
    return redirect(url_for('admin.list_employees'))


@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete a employee from the database
    """
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted employee.')

    # redirect to the employee page
    return redirect(url_for('admin.list_employees'))

    return render_template(title="Delete Employee")

# suppliers view

@admin.route('/suppliers')
@login_required
def list_suppliers():
    """
    List all suppliers
    """
    check_admin()

    suppliers = Supplier.query.all()
    return render_template('admin/suppliers/suppliers.html',
                           suppliers=suppliers, title='Suppliers')

@admin.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """
    Add a supplier to the database
    """
    check_admin()

    add_supplier = True

    form = SupplierForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_suppliers'))
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data)
        try:
            # add supplier to the database
            db.session.add(supplier)
            db.session.commit()
            flash('You have successfully added a new supplier.')
        except:
            # in case supplier name already exists
            flash('Error: supplier name already exists.')

        # redirect to supplier page
        return redirect(url_for('admin.list_suppliers'))

    # load supplier template
    return render_template('admin/suppliers/supplier.html', action="Add",
                           add_supplier=add_supplier, form=form,
                           title="Add Supplier")

@admin.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    """
    Edit a supplier
    """
    check_admin()

    add_supplier = False

    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    if form.cancel.data:
        return redirect(url_for('admin.list_suppliers'))

    if form.validate_on_submit():
        supplier.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the supplier.')

        # redirect to the supplier page
        return redirect(url_for('admin.list_suppliers'))

    form.name.data = supplier.name
    return render_template('admin/suppliers/supplier.html', action="Edit",
                           add_supplier=add_supplier, form=form,
                           supplier=supplier, title="Edit Supplier")

@admin.route('/suppliers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_supplier(id):
    """
    Delete a supplier from the database
    """
    check_admin()

    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('You have successfully deleted the supplier.')

    # redirect to the supplier page
    return redirect(url_for('admin.list_suppliers'))

    return render_template(title="Delete Supplier")

#units view

@admin.route('/units')
@login_required
def list_units():
    """
    List all units
    """
    check_admin()

    units = Unit.query.all()
    return render_template('admin/units/units.html',
                           units=units, title='Units')

@admin.route('/units/add', methods=['GET', 'POST'])
@login_required
def add_unit():
    """
    Add units to the database
    """
    check_admin()

    add_units = True

    form = UnitsForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_units'))

    if form.validate_on_submit():
        unit = Unit(unit_type=form.unit_type.data)
        try:
            # add unit to the database
            db.session.add(unit)
            db.session.commit()
            flash('You have successfully added a new unit.')
        except:
            # in case unit name already exists
            flash('Error: unit name already exists.')

        # redirect to unit page
        return redirect(url_for('admin.list_units'))

    # load unit template
    return render_template('admin/units/unit.html', action="Add",
                           add_unit=add_unit, form=form,
                           title="Add Unit")

@admin.route('/units/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_unit(id):
    """
    Edit unit
    """
    check_admin()

    add_unit = False

    unit = Unit.query.get_or_404(id)
    form = UnitsForm(obj=unit)
    if form.cancel.data:
        return redirect(url_for('admin.list_units'))

    if form.validate_on_submit():
        unit.unit_type = form.unit_type.data
        db.session.commit()
        flash('You have successfully edited the unit.')

        # redirect to the units page
        return redirect(url_for('admin.list_units'))

    form.unit_type.data = unit.unit_type
    return render_template('admin/units/unit.html', action="Edit",
                           add_unit=add_unit, form=form,
                           unit=unit, title="Edit Unit")

@admin.route('/units/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_unit(id):
    """
    Delete unit from the database
    """
    check_admin()

    unit = Unit.query.get_or_404(id)
    db.session.delete(unit)
    db.session.commit()
    flash('You have successfully deleted the unit.')

    # redirect to the units page
    return redirect(url_for('admin.list_units'))

    return render_template(title="Delete Unit")

#Consumables view

@admin.route('/consumables')
@login_required
def list_consumables():
    """
    List all consumables
    """
    check_admin()

    consumables = Consumable.query.all()
    return render_template('admin/consumables/consumables.html',
                           consumables=consumables, title='Consumables')


@admin.route('/consumables/add', methods=['GET', 'POST'])
@login_required
def add_consumable():
    """
    Add consumables to the database
    """
    check_admin()


    add_consumable = True
    form = ConsumableForm()

    if form.cancel.data:
        return redirect(url_for('admin.list_consumables'))
    if form.validate_on_submit():


        unity = form['unit_id'].data
        suppliery = form['supplier_id'].data
        curr_user = current_user.id

        consumable = Consumable()
        consumable.name=form.name.data,
        consumable.quantity=form.quantity.data,
        consumable.min_stock=form.min_stock.data,
        consumable.description=form.description.data,
        consumable.unit_id=unity.id,
        consumable.supplier_id=suppliery.id,
        consumable.user_id=curr_user

        try:
            # add consumable to the database
            db.session.add(consumable)
            db.session.commit()

            flash('You have successfully added a new consumable.')
        except:
            # in case consumable name already exists
            flash('Error: consumable name already exists.')

        # redirect to consumable page
        return redirect(url_for('admin.list_consumables'))

    # load consumable template
    return render_template('admin/consumables/consumable.html', action="Add",
                           add_consumable=add_consumable, form=form,
                           title="Add Consumable")


@admin.route('/consumables/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_consumables(id):
    """
    Edit consumable
    """
    check_admin()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    form = ConsumableForm(obj=consumable)
    unity = form['unit_id'].data
    suppliery = form['supplier_id'].data
    if form.cancel.data:
        return redirect(url_for('admin.list_consumables'))

    if form.validate_on_submit():

        consumable.name=form.name.data,
        consumable.quantity=form.quantity.data,
        consumable.min_stock=form.min_stock.data,
        consumable.description=form.description.data,
        consumable.unit_id=unity.id,
        consumable.supplier_id=suppliery.id

        db.session.commit()

        flash('You have successfully edited the consumable.')

        # redirect to the consumables page
        return redirect(url_for('admin.list_consumables'))

    return render_template('admin/consumables/consumable.html', action="Edit",
                           add_consumable=add_consumable, form=form,
                           consumable=consumable, title="Edit Consumable")


@admin.route('/consumables/consumption/<int:id>', methods=['GET', 'POST'])
@login_required
def consumption_consumables(id):
    """
    Consumption consumable
    """
    check_admin()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    consumption = consumable.quantity
    form = ConsumableConsumptionForm(obj=consumable)
    form.quantity.data = ""

    if form.cancel.data:
        return redirect(url_for('admin.list_consumables'))

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
        return redirect(url_for('admin.list_consumables'))

    return render_template('admin/consumables/consumable.html', action="Edit",
                           add_consumable=add_consumable, form=form,
                           consumable=consumable, title="Consumption Consumable")


@admin.route('/consumables/delivery/<int:id>', methods=['GET', 'POST'])
@login_required
def delivery_consumables(id):
    """
    Delivery consumable
    """
    check_admin()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    delivery = consumable.quantity
    form = ConsumableDeliveryForm(obj=consumable)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('admin.list_consumables'))

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
        return redirect(url_for('admin.list_consumables'))

    return render_template('admin/consumables/consumable.html', action="Edit",
                           add_consumable=add_consumable, form=form,
                           consumable=consumable, title="Delivery Consumable")


@admin.route('/consumables/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_consumables(id):
    """
    Delete consumable from the database
    """
    check_admin()

    consumable = Consumable.query.get_or_404(id)
    db.session.delete(consumable)
    db.session.commit()
    flash('You have successfully deleted the consumable.')

    # redirect to the units page
    return redirect(url_for('admin.list_consumables'))

    return render_template(title="Delete Consumable")


@admin.route('/consumable/details/<int:id>', methods=['GET', 'POST'])
@login_required
def details_consumable(id):
    "Details one consumable"

    check_admin()

    add_consumable = False

    consumable = Consumable.query.get_or_404(id)
    consumption = db.session.query(ConsumableConsumption).filter(ConsumableConsumption.consumab_id==consumable.id).order_by(ConsumableConsumption.date.desc()).all()
    delivers = db.session.query(ConsumableDelivery).filter(ConsumableDelivery.consumable_id==consumable.id).order_by(ConsumableDelivery.date.desc()).all()

    return render_template('admin/consumable_details/consumable_details.html',
                        consumable=consumable, consumption=consumption, delivers=delivers, title='Details consumable')

# Parcel view

@admin.route('/parcels')
@login_required
def list_parcels():
    """
    List all parcels
    """
    check_admin()

    parcels = Parcel.query.all()
    return render_template('admin/parcels/parcels.html',
                           parcels=parcels, title='Parcels')


@admin.route('/parcels/add', methods=['GET', 'POST'])
@login_required
def add_parcel():
    """
    Add parcels to the database
    """
    check_admin()

    add_parcels = True

    form = ParcelForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_parcels'))
    if form.validate_on_submit():
        parcel = Parcel(
        name=form.name.data,
        weight=form.weight.data,
        dimension=form.dimension.data,
        type=form.type.data
        )
        try:
            # add parcel to the database
            db.session.add(parcel)
            db.session.commit()
            flash('You have successfully added a new parcel.')
        except:
            # in case parcel name already exists
            flash('Error: parcel name already exists.')

        # redirect to parcel page
        return redirect(url_for('admin.list_parcels'))

    # load parcel template
    return render_template('admin/parcels/parcel.html', action="Add",
                           add_parcel=add_parcel, form=form,
                           title="Add Parcel")

@admin.route('/parcels/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_parcels(id):
    """
    Edit a parcel
    """
    check_admin()

    add_parcel = False

    parcel = Parcel.query.get_or_404(id)
    form = ParcelForm(obj=parcel)
    if form.cancel.data:
        return redirect(url_for('admin.list_parcels'))
    if form.validate_on_submit():
        parcel.name = form.name.data,
        parcel.weight=form.weight.data,
        parcel.dimension=form.dimension.data,
        parcel.type = form.type.data
        db.session.commit()
        flash('You have successfully edited the parcel.')

        # redirect to the parcels page
        return redirect(url_for('admin.list_parcels'))
        #
        # form.name.data = parcel.name,
        # form.type = parcel.type
    return render_template('admin/parcels/parcel.html', action="Edit",
                           add_parcel=add_parcel, form=form,
                           parcel=parcel, title="Edit Parcel")

@admin.route('/parcel/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_parcel(id):
    """
    Delete parcel from the database
    """
    check_admin()

    parcel = Parcel.query.get_or_404(id)
    db.session.delete(parcel)
    db.session.commit()
    flash('You have successfully deleted the parcel.')

    # redirect to the parcel page
    return redirect(url_for('admin.list_parcels'))

# Condition view

@admin.route('/conditions', methods=['GET', "POST"])
@login_required
def list_conditions():
    """
    List all conditions
    """

    conditions = Condition.query.all()

    return render_template('admin/conditions/conditions.html',
    conditions=conditions, title="Conditions")

@admin.route('/conditions/add', methods=['GET', 'POST'])
@login_required
def add_condition():
    """
    Add condition to the database
    """
    check_admin()

    add_condition = True

    form = ConditionForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_conditions'))
    if form.validate_on_submit():
        condition = Condition(
        name=form.name.data
        )
        try:
            # add condition to the database
            db.session.add(condition)
            db.session.commit()
            flash('You have successfully added a new condition.')
        except:
            # in case condition name already exists
            flash('Error: condition name already exists.')

        # redirect to condition page
        return redirect(url_for('admin.list_conditions'))
    # load parcel template
    return render_template('admin/conditions/condition.html', action="Add",
                           add_condition=add_condition, form=form,
                           title="Add Condition")

@admin.route('/conditions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_conditions(id):
    """
    Edit a condition
    """
    check_admin()

    add_parcel = False

    condition = Condition.query.get_or_404(id)
    form = ConditionForm(obj=condition)
    if form.cancel.data:
        return redirect(url_for('admin.list_conditions'))
    if form.validate_on_submit():
        condition.name = form.name.data,
        db.session.commit()
        flash('You have successfully edited the condition.')

        # redirect to the conditions page
        return redirect(url_for('admin.list_conditions'))

    return render_template('admin/conditions/condition.html', action="Edit",
                           add_condition=add_condition, form=form,
                           condition=condition, title="Edit Condition")

@admin.route('/conditions/condition/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_condition(id):
    """
    Delete condition from the database
    """
    check_admin()

    condition = Condition.query.get_or_404(id)
    db.session.delete(condition)
    db.session.commit()
    flash('You have successfully deleted the condition.')

    # redirect to the condition page
    return redirect(url_for('admin.list_conditions'))


# Direction view

@admin.route('/directions')
@login_required
def list_directions():
    """
    List all directions
    """
    check_admin()

    directions = Direction.query.all()
    return render_template('admin/directions/directions.html',
                           directions=directions, title='Directions')

@admin.route('/directions/add', methods=['GET', 'POST'])
@login_required
def add_directions():
    """
    Add directions to the database
    """
    check_admin()

    add_direction = True

    form = DirectionForm()
    if form.cancel.data:
        return redirect(url_for('admin.list_directions'))
    if form.validate_on_submit():
        direction = Direction(name=form.name.data)
        try:
            # add direction to the database
            db.session.add(direction)
            db.session.commit()
            flash('You have successfully added a new direction.')
        except:
            # in case direction name already exists
            flash('Error: direction name already exists.')

        # redirect to direction page
        return redirect(url_for('admin.list_directions'))

    # load direction template
    return render_template('admin/directions/direction.html', action="Add",
                           add_direction=add_direction, form=form,
                           title="Add Direction")

@admin.route('/directions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_directions(id):
    """
    Edit directions
    """
    check_admin()

    add_direction = False

    direction = Direction.query.get_or_404(id)
    form = DirectionForm(obj=direction)
    if form.cancel.data:
        return redirect(url_for('admin.list_directions'))
    if form.validate_on_submit():
        direction.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the direction.')

        # redirect to the directions page
        return redirect(url_for('admin.list_directions'))

    # form.unit_type.data = unit.unit_type
    return render_template('admin/directions/direction.html', action="Edit",
                           add_direction=add_direction, form=form,
                           direction=direction, title="Edit Direction")

@admin.route('/directions/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_direction(id):
    """
    Delete direction from the database
    """
    check_admin()

    direction = Direction.query.get_or_404(id)
    db.session.delete(direction)
    db.session.commit()
    flash('You have successfully deleted the direction.')

    # redirect to the direction page
    return redirect(url_for('admin.list_directions'))

    return render_template(title="Delete Direction")

# package view

@admin.route('/packages')
@login_required
def list_packages():
    """
    List all packages
    """
    check_admin()

    packages = Package.query.order_by(Package.description.asc()).all()
    return render_template('admin/packages/packages.html',
                           packages=packages, title='Packages')



@admin.route('/packages/add', methods=['GET', 'POST'])
@login_required
def add_package():
    """
    Add package to the database
    """
    check_admin()


    add_package = True
    form = PackageForm()

    if form.cancel.data:
        return redirect(url_for('admin.list_packages'))
    if form.validate_on_submit():


        parcely = form['parcel_id'].data

        package = Package()
        package.parcel_id=parcely.id
        package.quantity=form.quantity.data
        package.outside=0,
        package.inside=0,
        package.description=form.description.data,


        try:
            # add package to the database
            db.session.add(package)
            db.session.commit()

            flash('You have successfully added a new package.')
        except:
            # in case package name already exists
            flash('Error: package name already exists.')

        # redirect to package page
        return redirect(url_for('admin.list_packages'))

    # load consumable template
    return render_template('admin/packages/package.html', action="Add",
                           add_package=add_package, form=form,
                           title="Add Package")


@admin.route('/packages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_package(id):
    """
    Edit package to the database
    """
    check_admin()


    add_package = False
    package = Package.query.get_or_404(id)
    form = PackageFormEdit(obj=package)

    if form.cancel.data:
        return redirect(url_for('admin.list_packages'))
    if form.validate_on_submit():

        quantity = form['quantity'].data
        ins = form['inside'].data
        sumOut = quantity - ins


        package.outside=sumOut,
        package.inside=ins,
        package.quantity=quantity

        package.description=form.description.data,

        db.session.commit()

        flash('You have successfully edited a package.')

        # redirect to package page
        return redirect(url_for('admin.list_packages'))

    # load consumable template
    return render_template('admin/packages/package.html', action="Edit",
                           add_package=add_package, form=form,
                           title="Edit Package")


@admin.route('/packages/delivery/<int:id>', methods=['GET', 'POST'])
@login_required
def delivery_packages(id):
    """
    Delivery packages
    """
    check_admin()

    add_package = False

    package = Package.query.get_or_404(id)
    delivery = package.quantity

    form = PackageDeliveryForm(obj=package)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('admin.list_packages'))

    if form.validate_on_submit():

        now = datetime.now()
        curr_user = current_user.id
        suppliery = form['supplier_id'].data
        # parcel = form['parcel_id'].data

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
        return redirect(url_for('admin.list_packages'))

    return render_template('admin/packages/package.html', action="Edit",
                           add_package=add_package, form=form,
                           package=package, title="Delivery Package")


@admin.route('/packages/send/<int:id>', methods=['GET', 'POST'])
@login_required
def send_packages(id):
    """
    Send packages
    """
    check_admin()

    add_package = False

    package = Package.query.get_or_404(id)

    form = PackageDeliveryForm(obj=package)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('admin.list_packages'))

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
        return redirect(url_for('admin.list_packages'))

    return render_template('admin/packages/package.html', action="Edit",
                           add_package=add_package, form=form,
                           package=package, title="Send Package")

# receive package
@admin.route('/packages/receive/<int:id>', methods=['GET', 'POST'])
@login_required
def receive_packages(id):
    """
    Receive packages
    """
    check_admin()

    add_package = False

    package = Package.query.get_or_404(id)
    condition = Condition.query.all()

    form = PackageReceiveForm(obj=package)
    form.quantity.data = ""
    if form.cancel.data:
        return redirect(url_for('admin.list_packages'))

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
        return redirect(url_for('admin.list_packages'))

    return render_template('admin/packages/package.html', action="Add",
                           add_package=add_package, form=form,
                           package=package, title="Receive Package")

# pdf report
#
#
#
#
#
#


@admin.route('/packages/packages_details/packages_details/<int:id>', methods=['GET', 'POST'])
@login_required
def details_packages(id):
    "Details one package"

    check_admin()

    add_package = False

    package = Package.query.get_or_404(id)
    # consumption = db.session.query(ConsumableConsumption).filter(ConsumableConsumption.consumab_id==consumable.id).order_by(ConsumableConsumption.date.desc()).all()
    delivers = db.session.query(PackageDelivery).filter(PackageDelivery.package_id==package.id).order_by(PackageDelivery.date.desc()).all()

    return render_template('admin/packages/packages_details/packages_details.html',
                        package=package, delivers=delivers, title='Details package')


@admin.route('/packages/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_package(id):
    """
    Delete packages from the database
    """
    check_admin()

    package = Package.query.get_or_404(id)
    db.session.delete(package)
    db.session.commit()
    flash('You have successfully deleted package.')

    # redirect to the direction page
    return redirect(url_for('admin.list_packages'))
