from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Unit, Supplier, Employee

class ConsumableForm(FlaskForm):
    """
    Form for admin to add or edit a consumables
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
