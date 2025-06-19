from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FloatField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields import FieldList, FormField

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
    submit = SubmitField('Submit')

class FundingTypeForm(FlaskForm):
    Type = SelectField('Funding Type', choices=[(None, 'Select Type'), ('Loan', 'Loan'), ('Grant', 'Grant')], default=None, validators=[Optional()])
    Amount_KES = FloatField('Funding Amount (KES)', validators=[Optional()])

class FundingForm(FlaskForm):
    SourceID = SelectField('Source of Funds', coerce=coerce_to_int_or_none, default=None, validators=[Optional()])  # Populated dynamically with FundingSource.SourceID
    Amount_KES = FloatField('Funding Amount (KES)', validators=[Optional()])

class FinancialDetailForm(FlaskForm):
    Category = SelectField('Financial Category', choices=[
        (None, 'Select Category'),
        ('TotalContractSum', 'Total Contract Sum'),
        ('CumulativeExpenditure', 'Cumulative Expenditure'),
        ('OutstandingCost', 'Outstanding Cost'),
        ('ExchequerReleases', 'Exchequer Releases'),
        ('PendingBills', 'Pending Bills'),
        ('Savings', 'Savings'),
        ('ApprovedBudgetFY2021_22', 'Approved Budget FY 2021/22'),
        ('ApprovedBudgetFY2022_23', 'Approved Budget FY 2022/23'),
        ('ApprovedBudgetFY2023_24', 'Approved Budget FY 2023/24'),
        ('BudgetAllocationFY2024_25', 'Budget Allocation FY 2024/25'),
        ('BudgetAllocationFY2025_26', 'Budget Allocation FY 2025/26')
    ], default=None, validators=[Optional()])
    GoK_KES = FloatField('GoK Amount (KES)', validators=[Optional()])
    Foreign_KES = FloatField('Foreign Amount (KES)', validators=[Optional()])

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
    IntakeCapacity_m3 = FloatField('Intake Capacity (m³/day)', validators=[Optional()])
    TreatmentCapacity_m3 = FloatField('Treatment Capacity (m³/day)', validators=[Optional()])
    StorageCapacity_m3 = FloatField('Storage Capacity (m³)', validators=[Optional()])
    TreatedWaterMains_km = FloatField('Treated Water Mains (km)', validators=[Optional()])
    DistributionLines_km = FloatField('Distribution Lines (km)', validators=[Optional()])
    NumberOfWaterKiosks = IntegerField('Number of Water Kiosks/Communal Points', validators=[Optional()])
    NumberOfConnections = IntegerField('Number of Water Connections', validators=[Optional()])
    WastewaterCapacity_m3 = FloatField('Wastewater Production Capacity (m³/day)', validators=[Optional()])
    WastewaterTreatmentCapacity_m3 = FloatField('Wastewater Treatment Capacity (m³/day)', validators=[Optional()])
    TrunkSewerMain_km = FloatField('Trunk Sewer Main (km)', validators=[Optional()])
    ReticulationSewer_km = FloatField('Reticulation Sewer (km)', validators=[Optional()])
    Manholes = IntegerField('Number of Manholes', validators=[Optional()])
    NonSeweredSanitationFacilities = IntegerField('Number of Non-Sewered Sanitation Facilities', validators=[Optional()])
    SewerConnections_Households = IntegerField('Number of Sewer Connections (Households)', validators=[Optional()])
    TargetAreas = StringField('Target Areas', validators=[Optional()])
    TargetBeneficiaries_Households = IntegerField('Target Beneficiaries (Households)', validators=[Optional()])
    TargetBeneficiaries_Population = IntegerField('Target Beneficiaries (Population)', validators=[Optional()])
    Contractor = StringField('Contractor', validators=[Optional()])
    Consultant = StringField('Consultant', validators=[Optional()])
    StartDate = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    PlannedEndDate = DateField('Planned End Date', format='%Y-%m-%d', validators=[Optional()])
    ActualEndDate = DateField('Actual End Date', format='%Y-%m-%d', validators=[Optional()])
    ProgressPercentage = FloatField('Progress Percentage (%)', validators=[Optional()])
    ImpactsOfTheProject = TextAreaField('Impacts of the Project', validators=[Optional()])
    KeyChallenges = TextAreaField('Key Challenges', validators=[Optional()])
    Remarks = TextAreaField('Remarks', validators=[Optional()])
    funding_types = FieldList(FormField(FundingTypeForm), min_entries=1, max_entries=10, validators=[Optional()])
    fundings = FieldList(FormField(FundingForm), min_entries=1, max_entries=22, validators=[Optional()])
    financial_details = FieldList(FormField(FinancialDetailForm), min_entries=1, max_entries=11, validators=[Optional()])
    submit = SubmitField('Submit')