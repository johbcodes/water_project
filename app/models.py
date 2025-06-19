from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric, Enum
from datetime import datetime
from flask_login import UserMixin
from . import db 

class County(db.Model):
    __tablename__ = 'Counties'
    CountyID = db.Column(db.Integer, primary_key=True)
    CountyName = db.Column(db.String(100), nullable=False)
    constituencies = db.relationship('Constituency', backref='county', lazy=True)
    projects = db.relationship('Project', backref='county', lazy='select')

class Constituency(db.Model):
    __tablename__ = 'Constituencies'
    ConstituencyID = db.Column(db.Integer, primary_key=True)
    ConstituencyName = db.Column(db.String(100), nullable=False)
    CountyID = db.Column(db.Integer, db.ForeignKey('Counties.CountyID'), nullable=False)
    wards = db.relationship('Ward', backref='constituency', lazy=True)
    projects = db.relationship('Project', backref='constituency', lazy='select')

class Ward(db.Model):
    __tablename__ = 'Wards'
    WardID = db.Column(db.Integer, primary_key=True)
    WardName = db.Column(db.String(100), nullable=False)
    ConstituencyID = db.Column(db.Integer, db.ForeignKey('Constituencies.ConstituencyID'), nullable=False)
    projects = db.relationship('Project', backref='ward', lazy='select')

class FundingSource(db.Model):
    __tablename__ = 'FundingSources'
    SourceID = db.Column(db.Integer, primary_key=True)
    SourceName = db.Column(db.String(50), nullable=False, unique=True)  # e.g., GoK, AFD, KOICA
    fundings = db.relationship('Funding', backref='source', lazy=True)

class FundingType(db.Model):
    __tablename__ = 'FundingTypes'
    FundingTypeID = db.Column(db.Integer, primary_key=True)
    ProjectID = db.Column(db.Integer, db.ForeignKey('Projects.ProjectID'), nullable=False)
    Type = db.Column(Enum('Loan', 'Grant'), nullable=False)
    Amount_KES = db.Column(Numeric(15, 2), nullable=True)
    project = db.relationship('Project', backref='funding_types', lazy='select')

class Funding(db.Model):
    __tablename__ = 'Funding'
    FundingID = db.Column(db.Integer, primary_key=True)
    ProjectID = db.Column(db.Integer, db.ForeignKey('Projects.ProjectID'), nullable=False)
    SourceID = db.Column(db.Integer, db.ForeignKey('FundingSources.SourceID'), nullable=False)
    Amount_KES = db.Column(Numeric(15, 2), nullable=True)
    project = db.relationship('Project', backref='fundings', lazy='select')

class FinancialDetail(db.Model):
    __tablename__ = 'FinancialDetails'
    FinancialID = db.Column(db.Integer, primary_key=True)
    ProjectID = db.Column(db.Integer, db.ForeignKey('Projects.ProjectID'), nullable=False)
    Category = db.Column(Enum(
        'TotalContractSum', 'CumulativeExpenditure', 'OutstandingCost', 
        'ExchequerReleases', 'PendingBills', 'Savings',
        'ApprovedBudgetFY2021_22', 'ApprovedBudgetFY2022_23', 
        'ApprovedBudgetFY2023_24', 'BudgetAllocationFY2024_25', 
        'BudgetAllocationFY2025_26'
    ), nullable=False)
    GoK_KES = db.Column(Numeric(15, 2), nullable=True)
    Foreign_KES = db.Column(Numeric(15, 2), nullable=True)
    project = db.relationship('Project', backref='financial_details', lazy='select')

class SewerageInfrastructure(db.Model):
    __tablename__ = 'SewerageInfrastructure'
    SewerageID = db.Column(db.Integer, primary_key=True)
    ProjectID = db.Column(db.Integer, db.ForeignKey('Projects.ProjectID'), nullable=False)
    WastewaterTreatmentCapacity_m3 = db.Column(Numeric(10, 2), nullable=True)
    TrunkSewerMain_km = db.Column(Numeric(10, 2), nullable=True)
    ReticulationSewer_km = db.Column(Numeric(10, 2), nullable=True)
    Manholes = db.Column(db.Integer, nullable=True)
    NonSeweredSanitationFacilities = db.Column(db.Integer, nullable=True)
    SewerConnections_Households = db.Column(db.Integer, nullable=True)
    project = db.relationship('Project', backref='sewerage_infrastructure', lazy='select')

class Project(db.Model):
    __tablename__ = 'Projects'
    ProjectID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Maps to S/No
    ImplementingAgency = db.Column(db.String(255), nullable=True)
    Program = db.Column(db.String(255), nullable=True)
    ProjectName = db.Column(db.String(255), nullable=True)
    CountyID = db.Column(db.Integer, db.ForeignKey('Counties.CountyID'), nullable=True)
    ConstituencyID = db.Column(db.Integer, db.ForeignKey('Constituencies.ConstituencyID'), nullable=True)
    WardID = db.Column(db.Integer, db.ForeignKey('Wards.WardID'), nullable=True)
    GPSCoordinates = db.Column(db.String(50), nullable=True)
    ProjectType = db.Column(db.String(100), nullable=True)  # e.g., borehole, dam, sewerage
    ProjectLocation = db.Column(Enum('Rural', 'Urban'), nullable=True)
    ScopeOfWorks = db.Column(db.Text, nullable=True)
    IntakeCapacity_m3 = db.Column(Numeric(10, 2), nullable=True)
    TreatmentCapacity_m3 = db.Column(Numeric(10, 2), nullable=True)
    StorageCapacity_m3 = db.Column(Numeric(10, 2), nullable=True)
    TreatedWaterMains_km = db.Column(Numeric(10, 2), nullable=True)
    DistributionLines_km = db.Column(Numeric(10, 2), nullable=True)
    NumberOfWaterKiosks = db.Column(db.Integer, nullable=True)
    NumberOfConnections = db.Column(db.Integer, nullable=True)
    WastewaterCapacity_m3 = db.Column(Numeric(10, 2), nullable=True)
    TargetAreas = db.Column(db.String(255), nullable=True)
    TargetBeneficiaries_Households = db.Column(db.Integer, nullable=True)
    TargetBeneficiaries_Population = db.Column(db.Integer, nullable=True)
    Contractor = db.Column(db.String(255), nullable=True)
    Consultant = db.Column(db.String(255), nullable=True)
    StartDate = db.Column(db.Date, nullable=True)
    PlannedEndDate = db.Column(db.Date, nullable=True)
    ActualEndDate = db.Column(db.Date, nullable=True)
    ProgressPercentage = db.Column(Numeric(5, 2), nullable=True)
    ImpactsOfTheProject = db.Column(db.Text, nullable=True)
    KeyChallenges = db.Column(db.Text, nullable=True)
    Remarks = db.Column(db.Text, nullable=True)

class Region(db.Model):
    __tablename__ = 'Regions'
    RegionID = db.Column(db.Integer, primary_key=True)
    RegionName = db.Column(db.String(100), nullable=False)
    water_usages = db.relationship('WaterUsage', backref='region', lazy=True)

class WaterUsage(db.Model):
    __tablename__ = 'WaterUsage'
    UsageID = db.Column(db.Integer, primary_key=True)
    RegionID = db.Column(db.Integer, db.ForeignKey('Regions.RegionID'), nullable=False)
    Usage = db.Column(db.Float, nullable=False)
    UsageDate = db.Column(db.DateTime, default=datetime.utcnow)

class WaterSource(db.Model):
    __tablename__ = 'WaterSources'
    SourceID = db.Column(db.Integer, primary_key=True)
    SourceType = db.Column(db.String(100), nullable=False)
    Capacity = db.Column(db.Float, nullable=False)
    UsageDate = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    Role = db.Column(Enum('Admin', 'Manager', 'Viewer'), nullable=False)

    def get_id(self):
        return str(self.UserID)