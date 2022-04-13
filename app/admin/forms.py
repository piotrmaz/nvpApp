from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Unit, Supplier, Employee, Parcel, Condition, Direction

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class SupplierForm(FlaskForm):
    """
    Form for admin to add or edit a suppliers
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class UnitsForm(FlaskForm):
    """
    Form for admin to add or edit a units
    """
    unit_type = StringField('Unit Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class ConsumableForm(FlaskForm):
    """
    Form for admin to add or edit a consumables
    """
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    min_stock = IntegerField('Minimum stock')
    description = StringField('Description', validators=[DataRequired()])
    unit_id = QuerySelectField(query_factory=lambda: Unit.query.all(), get_label="unit_type")
    supplier_id = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')


class ConsumableConsumptionForm(FlaskForm):
    """
    Form for admin to add consumables consumption
    """
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class ConsumableDeliveryForm(FlaskForm):
    """
    Form for admin to add consumables delivery
    """
    quantity = IntegerField('Quantity')
    supplier_id = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')


class ParcelForm(FlaskForm):

    """
    Form for admin to add or edit a parcels
    """
    name = StringField('Name', validators=[DataRequired()])
    weight = IntegerField('Weight/pcs/kg')
    dimension = StringField('Dimension')
    type = SelectField('Type', choices = [('wood', 'wood'), ('plastic', 'plastic'), ('metal', 'metal')] )
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class ConditionForm(FlaskForm):
    """
    Form for admin to add or edit condition
    """

    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class DirectionForm(FlaskForm):
    """
    Form for admin to add or edit directions
    """

    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class PackageForm(FlaskForm):
    """
    Form for admin to add
    """

    parcel_id = QuerySelectField(query_factory=lambda: Parcel.query.all(), get_label="name")
    quantity = IntegerField('Quantity')
    # inside = IntegerField('Inside')
    # outside = IntegerField('Outside')
    description = StringField('Description')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class PackageFormEdit(FlaskForm):
    """
    Form for admin to edit
    """

    quantity = IntegerField('Quantity')
    inside = IntegerField('Inside')
    description = StringField('Description')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class PackageReceiveForm(FlaskForm):
    """
    Form for admin to receive packages
    """

    quantity = IntegerField('Quantity')
    condition = QuerySelectField(query_factory=lambda: Condition.query.all(), get_label="name")
    supplier = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    description = StringField('Description')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class PackageDeliveryForm(FlaskForm):
    """
    Form for admin to add packages delivery
    """
    # parcel_id = QuerySelectField(query_factory=lambda: Parcel.query.all(), get_label="name")
    supplier_id = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    quantity = IntegerField('Quantity')
    description = StringField('Description')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')
