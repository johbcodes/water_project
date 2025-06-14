from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, IntegerField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Optional

# Custom coercion function to handle None
def coerce_to_int_or_none(value):
    if value is None or value == 'None':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Viewer', 'Viewer')], validators=[DataRequired()])
    submit = SubmitField('Submit')  # Ensure this field is defined

class ProjectForm(FlaskForm):
    ImplementingAgency = StringField('Implementing Agency', validators=[DataRequired()])
    Program = StringField('Program', validators=[DataRequired()])
    ProjectName = StringField('Project Name', validators=[DataRequired()])
    CountyID = SelectField('County', coerce=coerce_to_int_or_none, default=None, validators=[DataRequired()])
    ConstituencyID = SelectField('Constituency', coerce=coerce_to_int_or_none, default=None, validators=[Optional()])
    WardID = SelectField('Ward', coerce=coerce_to_int_or_none, default=None, validators=[Optional()])
    GPSCoordinates = StringField('GPS Coordinates', validators=[Optional()])
    ProjectType = StringField('Project Type', validators=[Optional()])
    ProjectLocation = SelectField('Project Location', choices=[(None, 'Select Location'), ('Urban', 'Urban'), ('Rural', 'Rural')], default=None, validators=[Optional()])
    ScopeOfWorks = TextAreaField('Scope of Works', validators=[Optional()])
    IntakeCapacity_m3 = FloatField('Intake Capacity (m³)', validators=[Optional()])
    TreatmentCapacity_m3 = FloatField('Treatment Capacity (m³)', validators=[Optional()])
    StorageCapacity_m3 = FloatField('Storage Capacity (m³)', validators=[Optional()])
    TreatedWaterMains_km = FloatField('Treated Water Mains (km)', validators=[Optional()])
    DistributionLines_km = FloatField('Distribution Lines (km)', validators=[Optional()])
    NumberOfWaterKiosks = IntegerField('Number of Water Kiosks', validators=[Optional()])
    NumberOfConnections = IntegerField('Number of Connections', validators=[Optional()])
    WastewaterCapacity_m3 = FloatField('Wastewater Capacity (m³)', validators=[Optional()])
    TargetAreas = StringField('Target Areas', validators=[Optional()])
    TargetBeneficiaries_Households = IntegerField('Target Beneficiaries (Households)', validators=[Optional()])
    TargetBeneficiaries_Population = IntegerField('Target Beneficiaries (Population)', validators=[Optional()])
    Contractor = StringField('Contractor', validators=[Optional()])
    Consultant = StringField('Consultant', validators=[Optional()])
    StartDate = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    PlannedEndDate = DateField('Planned End Date', format='%Y-%m-%d', validators=[Optional()])
    ActualEndDate = DateField('Actual End Date', format='%Y-%m-%d', validators=[Optional()])
    ProgressPercentage = FloatField('Progress Percentage', validators=[Optional()])
    TotalContractSum_KES = FloatField('Total Contract Sum (KES)', validators=[Optional()])
    CumulativeExpenditure_KES = FloatField('Cumulative Expenditure (KES)', validators=[Optional()])
    OutstandingCost_KES = FloatField('Outstanding Cost (KES)', validators=[Optional()])
    ExchequerReleases_KES = FloatField('Exchequer Releases (KES)', validators=[Optional()])
    SumOfPendingBills_KES = FloatField('Sum of Pending Bills (KES)', validators=[Optional()])
    ApprovedBudgetFY2021_22 = FloatField('Approved Budget FY 2021/22', validators=[Optional()])
    ApprovedBudgetFY2021_23 = FloatField('Approved Budget FY 2021/23', validators=[Optional()])
    ApprovedBudgetFY2022_23 = FloatField('Approved Budget FY 2022/23', validators=[Optional()])
    ApprovedBudgetFY2022_24 = FloatField('Approved Budget FY 2022/24', validators=[Optional()])
    ApprovedBudgetFY2023_24 = FloatField('Approved Budget FY 2023/24', validators=[Optional()])
    ApprovedBudgetFY2023_25 = FloatField('Approved Budget FY 2023/25', validators=[Optional()])
    BudgetAllocationFY2024_25 = FloatField('Budget Allocation FY 2024/25', validators=[Optional()])
    BudgetAllocationFY2024_26 = FloatField('Budget Allocation FY 2024/26', validators=[Optional()])
    SourceOfFunds = SelectField('Source of Funds', choices=[
        (None, 'Select Source'), ('GoK', 'GoK'), ('AFD', 'AFD'), ('ADB', 'ADB'), ('EU', 'EU'),
        ('EIB', 'EIB'), ('KfW', 'KfW'), ('Belgium', 'Belgium'), ('Italy', 'Italy'),
        ('Netherlands', 'Netherlands'), ('EXIMBank', 'EXIMBank'), ('WB', 'WB'), ('BADEA', 'BADEA'),
        ('JICA', 'JICA'), ('KOREA', 'KOREA'), ('OFID', 'OFID'), ('SAUDIARABIA', 'Saudi Arabia'),
        ('DANIDA', 'DANIDA')
    ], default=None, validators=[Optional()])
    FundingAmount = FloatField('Funding Amount (KES)', validators=[Optional()])  # Kept for potential future use
    GoK_KES = FloatField('GoK Funding Amount (KES)', validators=[Optional()])
    AFD_KES = FloatField('AFD Funding Amount (KES)', validators=[Optional()])
    ADB_KES = FloatField('ADB Funding Amount (KES)', validators=[Optional()])
    EU_KES = FloatField('EU Funding Amount (KES)', validators=[Optional()])
    EIB_KES = FloatField('EIB Funding Amount (KES)', validators=[Optional()])
    KfW_KES = FloatField('KfW Funding Amount (KES)', validators=[Optional()])
    Belgium_KES = FloatField('Belgium Funding Amount (KES)', validators=[Optional()])
    Italy_KES = FloatField('Italy Funding Amount (KES)', validators=[Optional()])
    Netherlands_KES = FloatField('Netherlands Funding Amount (KES)', validators=[Optional()])
    EXIMBank_KES = FloatField('EXIMBank Funding Amount (KES)', validators=[Optional()])
    WB_KES = FloatField('WB Funding Amount (KES)', validators=[Optional()])
    BADEA_KES = FloatField('BADEA Funding Amount (KES)', validators=[Optional()])
    JICA_KES = FloatField('JICA Funding Amount (KES)', validators=[Optional()])
    KOREA_KES = FloatField('KOREA Funding Amount (KES)', validators=[Optional()])
    OFID_KES = FloatField('OFID Funding Amount (KES)', validators=[Optional()])
    SAUDIARABIA_KES = FloatField('Saudi Arabia Funding Amount (KES)', validators=[Optional()])
    DANIDA_KES = FloatField('DANIDA Funding Amount (KES)', validators=[Optional()])
    ImpactsOfTheProject = TextAreaField('Impacts of the Project', validators=[Optional()])
    KeyChallenges = TextAreaField('Key Challenges', validators=[Optional()])
    Remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Submit')