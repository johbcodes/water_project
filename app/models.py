from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
from flask_login import UserMixin
from . import db  # Import db from __init__.py

class County(db.Model):
    __tablename__ = 'Counties'
    CountyID = db.Column(db.Integer, primary_key=True)
    CountyName = db.Column(db.String(100), nullable=False)
    constituencies = db.relationship('Constituency', backref='county', lazy=True)

class Constituency(db.Model):
    __tablename__ = 'Constituencies'
    ConstituencyID = db.Column(db.Integer, primary_key=True)
    ConstituencyName = db.Column(db.String(100), nullable=False)
    CountyID = db.Column(db.Integer, db.ForeignKey('Counties.CountyID'), nullable=False)
    wards = db.relationship('Ward', backref='constituency', lazy=True)

class Ward(db.Model):
    __tablename__ = 'Wards'
    WardID = db.Column(db.Integer, primary_key=True)
    WardName = db.Column(db.String(100), nullable=False)
    ConstituencyID = db.Column(db.Integer, db.ForeignKey('Constituencies.ConstituencyID'), nullable=False)

class Project(db.Model):
    __tablename__ = 'Projects'
    ProjectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ImplementingAgency = db.Column(db.String(255))
    Program = db.Column(db.String(255))
    ProjectName = db.Column(db.String(255))
    CountyID = db.Column(db.Integer, db.ForeignKey('Counties.CountyID'))
    ConstituencyID = db.Column(db.Integer, db.ForeignKey('Constituencies.ConstituencyID'))
    WardID = db.Column(db.Integer, db.ForeignKey('Wards.WardID'))
    GPSCoordinates = db.Column(db.String(50))
    ProjectType = db.Column(db.String(100))
    ProjectLocation = db.Column(db.Enum('Rural', 'Urban'))
    ScopeOfWorks = db.Column(db.Text)
    IntakeCapacity_m3 = db.Column(Numeric(10, 2))
    TreatmentCapacity_m3 = db.Column(Numeric(10, 2))
    StorageCapacity_m3 = db.Column(Numeric(10, 2))
    TreatedWaterMains_km = db.Column(Numeric(10, 2))
    DistributionLines_km = db.Column(Numeric(10, 2))
    NumberOfWaterKiosks = db.Column(db.Integer)
    NumberOfConnections = db.Column(db.Integer)
    WastewaterCapacity_m3 = db.Column(Numeric(10, 2))
    TargetAreas = db.Column(db.String(255))
    TargetBeneficiaries_Households = db.Column(db.Integer)
    TargetBeneficiaries_Population = db.Column(db.Integer)
    Contractor = db.Column(db.String(255))
    Consultant = db.Column(db.String(255))
    StartDate = db.Column(db.Date)
    PlannedEndDate = db.Column(db.Date)
    ActualEndDate = db.Column(db.Date)
    ProgressPercentage = db.Column(Numeric(5, 2))
    TotalContractSum_KES = db.Column(Numeric(15, 2))
    CumulativeExpenditure_KES = db.Column(Numeric(15, 2))
    OutstandingCost_KES = db.Column(Numeric(15, 2))
    ExchequerReleases_KES = db.Column(Numeric(15, 2))
    SumOfPendingBills_KES = db.Column(Numeric(15, 2))
    ApprovedBudgetFY2021_22 = db.Column(Numeric(15, 2))
    ApprovedBudgetFY2021_23 = db.Column(Numeric(15, 2))
    ApprovedBudgetFY2022_23 = db.Column(Numeric(15, 2))
    ApprovedBudgetFY2022_24 = db.Column(Numeric(15, 2))
    ApprovedBudgetFY2023_24 = db.Column(Numeric(15, 2))
    ApprovedBudgetFY2023_25 = db.Column(Numeric(15, 2))
    BudgetAllocationFY2024_25 = db.Column(Numeric(15, 2))
    BudgetAllocationFY2024_26 = db.Column(Numeric(15, 2))
    ImpactsOfTheProject = db.Column(db.Text)
    KeyChallenges = db.Column(db.Text)
    Remarks = db.Column(db.Text)

    county = db.relationship('County', backref='projects', lazy='select')
    constituency = db.relationship('Constituency', backref='projects', lazy='select')
    ward = db.relationship('Ward', backref='projects', lazy='select')
    funding = db.relationship('Funding', backref='project', uselist=False, lazy='select')

class Funding(db.Model):
    __tablename__ = 'funding'
    FundingID = db.Column(db.Integer, primary_key=True)
    ProjectID = db.Column(db.Integer, db.ForeignKey('Projects.ProjectID'), nullable=False)
    SourceOfFunds = db.Column(db.String(50), nullable=False)
    GoK_KES = db.Column(db.Float, nullable=True)
    AFD_KES = db.Column(db.Float, nullable=True)
    ADB_KES = db.Column(db.Float, nullable=True)
    EU_KES = db.Column(db.Float, nullable=True)
    EIB_KES = db.Column(db.Float, nullable=True)
    KfW_KES = db.Column(db.Float, nullable=True)
    Belgium_KES = db.Column(db.Float, nullable=True)
    Italy_KES = db.Column(db.Float, nullable=True)
    Netherlands_KES = db.Column(db.Float, nullable=True)
    EXIMBank_KES = db.Column(db.Float, nullable=True)
    WB_KES = db.Column(db.Float, nullable=True)
    BADEA_KES = db.Column(db.Float, nullable=True)
    JICA_KES = db.Column(db.Float, nullable=True)
    KOREA_KES = db.Column(db.Float, nullable=True)
    OFID_KES = db.Column(db.Float, nullable=True)
    SAUDIARABIA_KES = db.Column(db.Float, nullable=True)
    DANIDA_KES = db.Column(db.Float, nullable=True)

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
    Role = db.Column(db.Enum('Admin', 'Manager', 'Viewer'), nullable=False)

    def get_id(self):
        return str(self.UserID)