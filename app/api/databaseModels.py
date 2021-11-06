from app import db

class Vaccine(db.Model):
    id_vaccine = db.Column(db.Integer, primary_key = True)
    vaccine_name = db.Column(db.Text, nullable = False)
    target_disease = db.Column(db.Text, nullable = False)
    number_to_administer = db.Column(db.Integer, nullable = False)
    dosage_interval = db.Column(db.Integer, nullable = True)

class Vial(db.Model):
    id_vial = db.Column(db.Text, primary_key = True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id_vaccine'), nullable = False)