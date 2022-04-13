from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Unit, Supplier, Employee, Condition

class ConsumableForm(FlaskForm):
    """
    Form for users to add or edit a consumables
    """
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    unit_id = QuerySelectField(query_factory=lambda: Unit.query.all(), get_label="unit_type")
    supplier_id = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class ConsumableConsumptionForm(FlaskForm):
    """
    Form for users to add consumables consumption
    """
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class ConsumableDeliveryForm(FlaskForm):
    """
    Form for users to add consumables delivery
    """
    quantity = IntegerField('Quantity')
    supplier_id = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class PackageReceiveForm(FlaskForm):
    """
    Form for users to receive packages
    """

    quantity = IntegerField('Quantity')
    condition = QuerySelectField(query_factory=lambda: Condition.query.all(), get_label="name")
    supplier = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    description = StringField('Description')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class PackageDeliveryForm(FlaskForm):
    """
    Form for users to add packages delivery
    """
    supplier_id = QuerySelectField(query_factory=lambda: Supplier.query.all(), get_label="name")
    quantity = IntegerField('Quantity')
    description = StringField('Description')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')
