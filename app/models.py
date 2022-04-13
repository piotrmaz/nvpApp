from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    is_granted = db.Column(db.Boolean, default=False)
    cons_deliv = db.relationship('ConsumableDelivery', backref='consdelivery', lazy='dynamic')
    cons_consumpt = db.relationship('ConsumableConsumption', backref='user_consumption', lazy='dynamic')
    consumable_user_id = db.relationship('Consumable', backref='consumable_user', lazy='dynamic')
    package_delivery_id = db.relationship('PackageDelivery', backref='package_delivery', lazy='dynamic')
    package_send_employee = db.relationship('PackageSend', backref='package_send_employee', lazy='dynamic')
    package_receive_employee = db.relationship('PackageReceive', backref='package_receive_employee', lazy='dynamic')


    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

# Suppliers

class Supplier(db.Model):
    """
    Create Supplier table
    """

    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    consumable_supplier = db.relationship('Consumable', backref='supplier', lazy='dynamic')
    consumable_delivery_id = db.relationship('ConsumableDelivery', backref='supplier', lazy='dynamic')
    package_supplier_id = db.relationship('PackageDelivery', backref='package_supplier', lazy='dynamic')
    packages_send_supplier = db.relationship('PackageSend', backref='packages_send_supplier', lazy='dynamic')
    package_receive_supplier = db.relationship('PackageReceive', backref='packages_receive_supplier', lazy='dynamic')


    def __repr__(self):
        return '<Supplier: {}>'.format(self.name)


#Returnable packages

class Parcel(db.Model):
    """
    Create Parcel table
    """

    __tablename__= 'parcels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    weight = db.Column(db.Integer)
    dimension = db.Column(db.String(60))
    type = db.Column(db.String(60))
    package_parcels_id = db.relationship('Package', backref='parcel', lazy='dynamic')


    def __repr__(self):
        return '<Parcel: {}>'.format(self.name)

class Condition(db.Model):
    """
    Create Condition table
    """

    __tablename__= 'conditions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    package_receive_condition = db.relationship('PackageReceive', backref='package_condition', lazy='dynamic')

    def __repr__(self):
        return '<Condition: {}>'.format(self.name)

class Direction(db.Model):
    """
    Create Direction table
    """

    __tablename__= 'directions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def __repr__(self):
        return '<Direction: {}>'.format(self.name)

class Package(db.Model):
    """
    Creater Package table
    """

    __tablename__= 'packages'

    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcels.id'))
    quantity = db.Column(db.Integer)
    inside = db.Column(db.Integer)
    outside = db.Column(db.Integer)
    description = db.Column(db.String(200))
    package_delivery_id = db.relationship('PackageDelivery', backref='package_delivery_id', lazy='dynamic')
    packages_send_id = db.relationship('PackageSend', backref='packages_send_id', lazy='dynamic')
    package_receive_package_id = db.relationship('PackageReceive', backref='package_receive', lazy='dynamic')

    def __repr__(self):
        return '<Package: {}>'.format(self.name)

class PackageDelivery(db.Model):
    """
    Create PackageDelivery table
    """

    __tablename__='packagesDelivery'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class PackageSend(db.Model):
    """
    Create PackageSend table
    """

    __tablename__='packagesSend'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class PackageReceive(db.Model):
    """
    Create PackageReceive table
    """

    __tablename__='packagesReceive'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    condition = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<PackageReceive: {}>'.format(self.name)

#consumables
class Unit(db.Model):
    """
    Create Unit table
    """

    __tablename__= 'units'

    id = db.Column(db.Integer, primary_key=True)
    unit_type = db.Column(db.String(10))
    consumableses = db.relationship('Consumable', backref='consumable', lazy='joined')


    def __repr__(self):
        return '<Unit: {}>'.format(self.unit_type)



class Consumable(db.Model):
    """
    Create Comsumable table
    """

    __tablename__= 'consumables'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    consumption_consumable = db.relationship('ConsumableConsumption', backref='consumption_consumable', lazy='joined', cascade="all,delete")
    delivery_consumable = db.relationship('ConsumableDelivery', backref='delivery_consumable', lazy='joined', cascade="all,delete")
    min_stock = db.Column(db.Integer)

    def __repr__(self):
        return '<Consumable: {}>'.format(self.name)

class ConsumableDelivery(db.Model):
    """
    Create ConsumableDelivery table
    """

    __tablename__ = 'consum_delivery'

    id = db.Column(db.Integer, primary_key=True)
    consumable_id = db.Column(db.Integer, db.ForeignKey('consumables.id'))
    user_delivery_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    supplier_consumable_delivery_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<ConsumableDelivery: {}>'.format(self.name)

class ConsumableConsumption(db.Model):
    """
    Create ConsumableConsumption table
    """

    __tablename__ = 'consum_consumptions'

    id = db.Column(db.Integer, primary_key=True)
    consumab_id = db.Column(db.Integer, db.ForeignKey('consumables.id'))
    user_consumption_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<ConsumableConsumption: {}>'.format(self.id, self.consumab_id, self.user_consumption_id, self.quantity, self.date)
