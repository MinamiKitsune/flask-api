from app import db


class Vaccine(db.Model):
    id_vaccine = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.Text, nullable=False)
    target_disease = db.Column(db.Text, nullable=False)
    number_to_administer = db.Column(db.Integer, nullable=False)
    dosage_interval = db.Column(db.Integer, nullable=True)


class Vial(db.Model):
    id_vial = db.Column(db.Text, primary_key=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id_vaccine'), nullable=False)


class Citizen(db.Model):
    id_citizen = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    mobile_num = db.Column(db.Text, nullable=False)
    medical_aid = db.Column(db.Text, nullable=True)
    citizen_address = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Text, db.ForeignKey('citizen.id_citizen'), nullable=True)


class Location(db.Model):
    id_location = db.Column(db.Integer, primary_key=True)
    location_address = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    zip_code = db.Column(db.Text, nullable=False)
    name_of_place = db.Column(db.Text, nullable=False)


class Vaccination(db.Model):
    id_vaccination = db.Column(db.Text, primary_key=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey('citizen.id_citizen'), nullable=False)
    vial_id = db.Column(db.Text, db.ForeignKey('vial.id_vial'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id_location'), nullable=False)
    date_of_vaccination = db.Column(db.Date, nullable=False)
    dosage_number = db.Column(db.Integer, nullable=False)
    side_effects = db.Column(db.Boolean, nullable=False)
    description_side_effects = db.Column(db.Text, nullable=True)


class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Text, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
