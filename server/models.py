# Import necessary modules
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Initialize SQLAlchemy

#Patient Model
class Patient(db.Model):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Patient name
    address = db.Column(db.String(255))  # Patient address
    insurance = db.Column(db.String(100))  # Insurance type or company

     # Define the `to_dict()` method to convert the object to a dictionary, to be in frontend fetch the key you want
    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "insurance": self.insurance
        }
    # Serialize_rules
    prescriptions = db.relationship('Prescription', back_populates='patient')  # Relationship
    serialize_rules = ('-prescriptions',)  # Exclude prescriptions during serialization of Patient



#Pharmacist Model
class Pharmacist(db.Model):
    __tablename__ = 'pharmacist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Pharmacist name
    pharmacy = db.Column(db.String(100))  # Pharmacy name or affiliation

    # One-to-many relationship with Prescription
    prescriptions = db.relationship('Prescription', back_populates='pharmacist')

    # Convert to dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "pharmacy": self.pharmacy,
        }



#Drug Model:

class Drug(db.Model):
    __tablename__ = 'drug'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    ndc_id = db.Column(db.String(10), nullable=False, unique=True)  # Unique NDC identifier
    name = db.Column(db.String(100), nullable=False)  # Drug name
    description = db.Column(db.String(255))  # Description
    dosage_form = db.Column(db.String(50))  # Form (tablet, capsule, etc.)
    strength = db.Column(db.String(50))  # Drug strength
    
    # Relationship with Prescription model (one-to-many), but excluded from serialization
    prescriptions = db.relationship(
        "Prescription",
        back_populates="drug",
        lazy=True,  # Ensure the relationship is not eagerly loaded
    )

    # Custom `to_dict()` method that does not include the `prescriptions` relationship
    def to_dict(self):
        return {
            'id': self.id,
            'ndc_id': self.ndc_id,
            'name': self.name,
            'description': self.description,
            'dosage_form': self.dosage_form,
            'strength': self.strength,
        }




#Prescription Model 

class Prescription(db.Model):
    __tablename__ = 'prescription'

    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drug.id'))  # Foreign key to Drug
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))  # Correct reference
    pharmacist_id = db.Column(db.Integer, db.ForeignKey('pharmacist.id'))  # Foreign key to Pharmacist
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of prescription
    instructions = db.Column(db.String(255))  # Instructions for use
    status = db.Column(db.String(50), default='pending')  # Status of prescription

    # Relationships to link Prescription with other models
    drug = db.relationship('Drug', back_populates='prescriptions')  # Link to Drug
    patient = db.relationship('Patient')  # Link to Patient
    pharmacist = db.relationship('Pharmacist')  # Link to Pharmacist 

    # Define to_dict() Method
    def to_dict(self):
        return {
            "id": self.id,
            "drug_id": self.drug_id,
            "patient_id": self.patient_id,
            "pharmacist_id": self.pharmacist_id,
            "created_at": self.created_at,
            "instructions": self.instructions,
            "status": self.status,
            # Include related data from relationships, if desired
            "drug": self.drug.name if self.drug else None,
            "patient": {
                "id": self.patient.id,
                "name": self.patient.name,
            } if self.patient else None,
            "pharmacist": {
                "id": self.pharmacist.id,
                "name": self.pharmacist.name,
            } if self.pharmacist else None,
        }

    # serialize_rules
    patient = db.relationship('Patient', back_populates='prescriptions')   # Relationship
    serialize_rules = ('-patient',)  # Exclude patient during serialization of Prescription 