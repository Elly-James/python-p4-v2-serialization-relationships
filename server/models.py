# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin



# The 'convention' dictionary defines naming conventions for various database constraints and indexes
# These naming conventions are applied automatically when SQLAlchemy generates database constraints,
# indexes, and other elements, allowing for consistent and predictable names in the database schema.

convention = {
    # "ix" refers to indexes. The naming pattern for indexes will be 'ix_<column_name>'.
    # For example, if the column name is 'id', the index name would be 'ix_id'.
    "ix": "ix_%(column_0_label)s",  # %(column_0_label)s is replaced by the column name.

    # "uq" refers to unique constraints. The naming pattern for unique constraints will be
    # 'uq_<table_name>_<column_name>'.
    # For example, for the 'users' table and the 'email' column, the unique constraint name will be 'uq_users_email'.
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # %(table_name)s and %(column_0_name)s are replaced by table and column names.

    # "ck" refers to check constraints. The naming pattern for check constraints will be
    # 'ck_<table_name>_<constraint_name>'.
    # This is used when adding check constraints to ensure data integrity.
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # %(table_name)s and %(constraint_name)s are replaced by respective values.

    # "fk" refers to foreign key constraints. The naming pattern for foreign keys will be
    # 'fk_<table_name>_<column_name>_<referred_table_name>'.
    # For example, a foreign key on the 'user_id' column in the 'posts' table that refers to the 'users' table
    # would have the name 'fk_posts_user_id_users'.
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key relationships between tables.

    # "pk" refers to primary key constraints. The naming pattern for primary keys will be
    # 'pk_<table_name>'.
    # For example, the primary key for the 'users' table will be 'pk_users'.
    "pk": "pk_%(table_name)s"  # %(table_name)s is replaced by the table name.
}

# The 'MetaData' object is responsible for managing schema-related information in SQLAlchemy.
# The 'naming_convention' parameter is passed to it, applying the above naming conventions
# to the generated database schema objects (indexes, constraints, etc.).

metadata = MetaData(naming_convention=convention)  # MetaData object is created with custom naming conventions.


db = SQLAlchemy(metadata=metadata)


class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = 'zookeepers'

    # don't forget that every tuple needs at least one comma!
   # The 'serialize_rules' variable is typically used with libraries like Flask-SQLAlchemy or Marshmallow to control
# how database models are serialized (converted to JSON or other formats).

# In this case, the 'serialize_rules' variable is a tuple containing the string '-animals.zookeeper'.

# The rule '-animals.zookeeper' works as follows:
# - The minus sign ('-') before the attribute name ('animals.zookeeper') indicates exclusion.
# - In this case, the field 'zookeeper' from the related 'animals' model will be excluded from the serialized output.
# - Without the minus sign, the field would be included in the serialized output.

# 'animals.zookeeper' refers to a relationship or a field that is part of the 'animals' attribute of the model.
# In an ORM (like SQLAlchemy), this could represent a foreign key relationship or a nested object in the model.

# So, when serializing an object, if this rule is applied, the 'zookeeper' attribute within the 'animals' relationship
# will not be included in the resulting output (e.g., JSON response).



    serialize_rules = ('-animals.zookeeper',)  # Excludes the 'zookeeper' field in the 'animals' relationship from serialization


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birthday = db.Column(db.Date)

    animals = db.relationship('Animal', back_populates='zookeeper')


class Enclosure(db.Model, SerializerMixin):
    __tablename__ = 'enclosures'

    serialize_rules = ('-animals.enclosure',)

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)

    animals = db.relationship('Animal', back_populates='enclosure')


class Animal(db.Model, SerializerMixin):
    __tablename__ = 'animals'

    serialize_rules = ('-zookeeper.animals', '-enclosure.animals',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    enclosure = db.relationship('Enclosure', back_populates='animals')
    zookeeper = db.relationship('Zookeeper', back_populates='animals')

    def __repr__(self):
        return f'<Animal {self.name}, a {self.species}>'