from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from .models import County, Constituency, Ward, Project, Funding, WaterUsage, Region, WaterSource, User
from . import db
from flask_login import login_required, current_user, logout_user, login_user
from .forms import UserForm, ProjectForm, LoginForm
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import pandas as pd
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user and check_password_hash(user.Password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.Role == 'Admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.all()
    projects_data = [
        {
            "ProjectName": project.ProjectName,
            "ProgressPercentage": float(project.ProgressPercentage) if project.ProgressPercentage is not None else 0.0,
            "PlannedEndDate": project.PlannedEndDate.strftime('%Y-%m-%d') if project.PlannedEndDate else "TBD"
        } for project in projects
    ]
    avg_completion = round(sum(p["ProgressPercentage"] for p in projects_data) / len(projects_data), 1) if projects_data else 0.0
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('dashboard.html', projects=projects_data, current_date=current_date, avg_completion=avg_completion)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/get_counties', methods=['GET'])
@login_required
def get_counties():
    counties = County.query.order_by(County.CountyName).all()
    return jsonify([{'CountyID': c.CountyID, 'CountyName': c.CountyName} for c in counties])

@main.route('/get_constituencies/<int:county_id>', methods=['GET'])
@login_required
def get_constituencies(county_id):
    constituencies = Constituency.query.filter_by(CountyID=county_id).order_by(Constituency.ConstituencyName).all()
    return jsonify([{'ConstituencyID': c.ConstituencyID, 'ConstituencyName': c.ConstituencyName} for c in constituencies])

@main.route('/get_wards/<int:constituency_id>', methods=['GET'])
@login_required
def get_wards(constituency_id):
    wards = Ward.query.filter_by(ConstituencyID=constituency_id).order_by(Ward.WardName).all()
    return jsonify([{'WardID': w.WardID, 'WardName': w.WardName} for w in wards])

@main.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if current_user.Role not in ['Admin', 'Manager']:
        flash('You do not have permission to add projects.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = ProjectForm()
    counties = County.query.order_by(County.CountyName).all()
    form.CountyID.choices = [(None, 'Select County')] + [(str(county.CountyID), county.CountyName) for county in counties]
    form.ConstituencyID.choices = [(None, 'Select Constituency')]
    form.WardID.choices = [(None, 'Select Ward')]

    if request.method == 'POST':
        if form.CountyID.data and form.CountyID.data != 'None':
            constituencies = Constituency.query.filter_by(CountyID=int(form.CountyID.data)).order_by(Constituency.ConstituencyName).all()
            form.ConstituencyID.choices = [(None, 'Select Constituency')] + [(str(c.ConstituencyID), c.ConstituencyName) for c in constituencies]
        if form.ConstituencyID.data and form.ConstituencyID.data != 'None':
            wards = Ward.query.filter_by(ConstituencyID=int(form.ConstituencyID.data)).order_by(Ward.WardName).all()
            form.WardID.choices = [(None, 'Select Ward')] + [(str(w.WardID), w.WardName) for w in wards]

        if form.validate_on_submit():
            try:
                new_project = Project()
                form.populate_obj(new_project)
                new_project.ProjectName = new_project.ProjectName or "Unnamed Project"
                new_project.ImplementingAgency = new_project.ImplementingAgency or "Unknown"
                new_project.CountyID = int(form.CountyID.data) if form.CountyID.data and form.CountyID.data != 'None' else None
                new_project.ConstituencyID = int(form.ConstituencyID.data) if form.ConstituencyID.data and form.ConstituencyID.data != 'None' else None
                new_project.WardID = int(form.WardID.data) if form.WardID.data and form.WardID.data != 'None' else None

                db.session.add(new_project)
                db.session.flush()

                funding_map = {
                    'GoK': 'GoK_KES', 'AFD': 'AFD_KES', 'ADB': 'ADB_KES', 'EU': 'EU_KES',
                    'EIB': 'EIB_KES', 'KfW': 'KfW_KES', 'Belgium': 'Belgium_KES', 'Italy': 'Italy_KES',
                    'Netherlands': 'Netherlands_KES', 'EXIMBank': 'EXIMBank_KES', 'WB': 'WB_KES',
                    'BADEA': 'BADEA_KES', 'JICA': 'JICA_KES', 'KOREA': 'KOREA_KES', 'OFID': 'OFID_KES',
                    'SAUDIARABIA': 'SAUDIARABIA_KES', 'DANIDA': 'DANIDA_KES'
                }
                selected_source = form.SourceOfFunds.data
                selected_field = funding_map.get(selected_source)
                selected_amount = getattr(form, selected_field).data if selected_field else None
                if selected_source or selected_amount:
                    new_funding = Funding(ProjectID=new_project.ProjectID, SourceOfFunds=selected_source or "Unknown")
                    if selected_field and selected_amount is not None:
                        setattr(new_funding, selected_field, selected_amount)
                    db.session.add(new_funding)

                db.session.commit()
                flash('Project and funding added successfully!', 'success')
                return redirect(url_for('main.view_projects'))
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error adding project: {str(e)}", exc_info=True)
                flash(f'Error adding project: {str(e)}', 'danger')
        else:
            current_app.logger.error(f"Form validation failed: {form.errors}")
            flash(f'Please correct the errors in the form: {form.errors}', 'danger')

    return render_template('add_project.html', form=form)

@main.route('/view_projects')
@login_required
def view_projects():
    projects = Project.query.options(
        db.joinedload(Project.county),
        db.joinedload(Project.constituency),
        db.joinedload(Project.ward)
    ).all()
    funding_map = {
        'GoK': 'GoK_KES', 'AFD': 'AFD_KES', 'ADB': 'ADB_KES', 'EU': 'EU_KES',
        'EIB': 'EIB_KES', 'KfW': 'KfW_KES', 'Belgium': 'Belgium_KES', 'Italy': 'Italy_KES',
        'Netherlands': 'Netherlands_KES', 'EXIMBank': 'EXIMBank_KES', 'WB': 'WB_KES',
        'BADEA': 'BADEA_KES', 'JICA': 'JICA_KES', 'KOREA': 'KOREA_KES', 'OFID': 'OFID_KES',
        'SAUDIARABIA': 'SAUDIARABIA_KES', 'DANIDA': 'DANIDA_KES'
    }
    for project in projects:
        funding = Funding.query.filter_by(ProjectID=project.ProjectID).first()
        project.SourceOfFunds = funding.SourceOfFunds if funding else "Unknown"
        project.FundingAmount = getattr(funding, funding_map.get(project.SourceOfFunds), 0.0) if funding else 0.0

    return render_template('view_projects.html', projects=projects)

@main.route('/reports')
@login_required
def reports():
    projects = Project.query.all()
    projects_data = [{
        "ProjectID": project.ProjectID,
        "ProjectName": project.ProjectName,
        "ProgressPercentage": float(project.ProgressPercentage) if project.ProgressPercentage is not None else 0.0
    } for project in projects]
    return render_template('reports.html', projects=projects_data)

@main.route('/api/water_usage_by_region')
@login_required
def water_usage_by_region():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = db.session.query(
        Region.RegionName,
        db.func.sum(WaterUsage.Usage).label('TotalUsage')
    ).join(WaterUsage, Region.RegionID == WaterUsage.RegionID)
    if start_date and end_date:
        query = query.filter(WaterUsage.UsageDate.between(start_date, end_date))
    water_usage_data = query.group_by(Region.RegionName).all()
    data = [{"RegionName": row.RegionName, "TotalUsage": float(row.TotalUsage)} for row in water_usage_data]
    return jsonify(data)

@main.route('/api/water_source_distribution')
@login_required
def water_source_distribution():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = db.session.query(
        WaterSource.SourceType,
        db.func.sum(WaterSource.Capacity).label('TotalCapacity')
    ).group_by(WaterSource.SourceType)
    if start_date and end_date:
        query = query.filter(WaterSource.UsageDate.between(start_date, end_date))
    water_source_data = query.all()
    data = [{"SourceType": row.SourceType, "TotalCapacity": float(row.TotalCapacity)} for row in water_source_data]
    return jsonify(data)

@main.route('/api/real_time_water_usage')
@login_required
def real_time_water_usage():
    water_usage_data = WaterUsage.query.order_by(WaterUsage.UsageDate.desc()).limit(10).all()
    data = [{"UsageDate": row.UsageDate.strftime('%Y-%m-%d %H:%M:%S'), "Usage": float(row.Usage)} for row in water_usage_data]
    return jsonify(data)

@main.route('/api/project_progress')
@login_required
def project_progress():
    projects = Project.query.all()
    data = [{"ProjectName": project.ProjectName, "ProgressPercentage": float(project.ProgressPercentage) if project.ProgressPercentage is not None else 0.0} for project in projects]
    return jsonify(data)

@main.route('/admin/dashboard')
@login_required
def user_management():
    if current_user.Role != 'Admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    users = User.query.all()
    projects = Project.query.all()
    return render_template('user_management.html', users=users, projects=projects)

@main.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.Role != 'Admin':
        flash('You do not have permission to add users.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        existing_user = User.query.filter_by(Username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('add_user.html', form=form)

        new_user = User(
            Username=username,
            Password=generate_password_hash(form.password.data),
            Role=form.role.data
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully!', 'success')
            return redirect(url_for('main.user_management'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the user.', 'danger')
            print(f"Error: {e}")
            return render_template('add_user.html', form=form)

    return render_template('add_user.html', form=form)

@main.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.Role != 'Admin':
        flash('You do not have permission to edit users.', 'danger')
        return redirect(url_for('main.dashboard'))

    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        new_username = form.username.data
        existing_user = User.query.filter_by(Username=new_username).first()
        if existing_user and existing_user.UserID != user.UserID:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('edit_user.html', form=form, user=user)

        user.Username = new_username
        if form.password.data:
            user.Password = generate_password_hash(form.password.data)
        user.Role = form.role.data

        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('main.user_management'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the user.', 'danger')
            print(f"Error: {e}")

    if request.method == 'GET':
        form.username.data = user.Username
        form.role.data = user.Role
        form.password.data = ''

    return render_template('edit_user.html', form=form, user=user)

@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.Role != 'Admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('main.user_management'))

@main.route('/admin/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if current_user.Role != 'Admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))

    project = Project.query.get_or_404(project_id)
    funding = Funding.query.filter_by(ProjectID=project_id).first()

    form = ProjectForm(obj=project)
    form.CountyID.choices = [(None, 'Select County')] + [(str(county.CountyID), county.CountyName) for county in County.query.order_by(County.CountyName).all()]
    form.ConstituencyID.choices = [(None, 'Select Constituency')]
    form.WardID.choices = [(None, 'Select Ward')]

    funding_map = {
        'GoK': 'GoK_KES', 'AFD': 'AFD_KES', 'ADB': 'ADB_KES', 'EU': 'EU_KES',
        'EIB': 'EIB_KES', 'KfW': 'KfW_KES', 'Belgium': 'Belgium_KES', 'Italy': 'Italy_KES',
        'Netherlands': 'Netherlands_KES', 'EXIMBank': 'EXIMBank_KES', 'WB': 'WB_KES',
        'BADEA': 'BADEA_KES', 'JICA': 'JICA_KES', 'KOREA': 'KOREA_KES', 'OFID': 'OFID_KES',
        'SAUDIARABIA': 'SAUDIARABIA_KES', 'DANIDA': 'DANIDA_KES'
    }

    if request.method == 'POST':
        if form.CountyID.data and form.CountyID.data != 'None':
            form.ConstituencyID.choices = [(None, 'Select Constituency')] + [(str(c.ConstituencyID), c.ConstituencyName) for c in Constituency.query.filter_by(CountyID=int(form.CountyID.data)).all()]
        if form.ConstituencyID.data and form.ConstituencyID.data != 'None':
            form.WardID.choices = [(None, 'Select Ward')] + [(str(w.WardID), w.WardName) for w in Ward.query.filter_by(ConstituencyID=int(form.ConstituencyID.data)).all()]

        if form.validate_on_submit():
            try:
                form.populate_obj(project)
                project.CountyID = int(form.CountyID.data) if form.CountyID.data and form.CountyID.data != 'None' else None
                project.ConstituencyID = int(form.ConstituencyID.data) if form.ConstituencyID.data and form.ConstituencyID.data != 'None' else None
                project.WardID = int(form.WardID.data) if form.WardID.data and form.WardID.data != 'None' else None

                selected_source = form.SourceOfFunds.data
                selected_field = funding_map.get(selected_source)
                selected_amount = getattr(form, selected_field).data if selected_field else None

                if funding:
                    for field in funding_map.values():
                        setattr(funding, field, None)
                    if selected_field and selected_amount is not None:
                        setattr(funding, selected_field, selected_amount)
                    funding.SourceOfFunds = selected_source or "Unknown"
                else:
                    if selected_source or selected_amount:
                        new_funding = Funding(ProjectID=project.ProjectID, SourceOfFunds=selected_source or "Unknown")
                        if selected_field and selected_amount is not None:
                            setattr(new_funding, selected_field, selected_amount)
                        db.session.add(new_funding)

                db.session.commit()
                flash('Project and funding updated successfully!', 'success')
                return redirect(url_for('main.view_projects'))
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error updating project: {str(e)}", exc_info=True)
                flash(f'Error updating project: {str(e)}', 'danger')
        else:
            current_app.logger.error(f"Form validation failed: {form.errors}")
            flash(f'Please correct the errors in the form: {form.errors}', 'danger')

    if project.CountyID:
        form.CountyID.data = str(project.CountyID)
        form.ConstituencyID.choices = [(None, 'Select Constituency')] + [(str(c.ConstituencyID), c.ConstituencyName) for c in Constituency.query.filter_by(CountyID=project.CountyID).all()]
    if project.ConstituencyID:
        form.ConstituencyID.data = str(project.ConstituencyID)
        form.WardID.choices = [(None, 'Select Ward')] + [(str(w.WardID), w.WardName) for w in Ward.query.filter_by(ConstituencyID=project.ConstituencyID).all()]
    if project.WardID:
        form.WardID.data = str(project.WardID)
    if funding:
        form.SourceOfFunds.data = funding.SourceOfFunds
        for source, field in funding_map.items():
            amount = getattr(funding, field)
            if amount is not None:
                getattr(form, field).data = float(amount)

    return render_template('edit_project.html', form=form, project=project)



@main.route('/upload_projects_excel', methods=['GET', 'POST'])
@login_required
def upload_projects_excel():
    if current_user.Role not in ['Admin', 'Manager']:
        flash('You do not have permission to upload projects.', 'danger')
        return redirect(url_for('main.view_projects'))

    if request.method == 'POST':
        if 'excel_file' not in request.files:
            flash('No file part in the request.', 'danger')
            return redirect(url_for('main.view_projects'))

        file = request.files['excel_file']
        if not file or file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('main.view_projects'))

        if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            flash('Invalid file format. Please upload an Excel file (.xlsx or .xls).', 'danger')
            return redirect(url_for('main.view_projects'))

        try:
            excel_file = pd.ExcelFile(file, engine='openpyxl' if file.filename.endswith('.xlsx') else 'xlrd')
            sheet_names = excel_file.sheet_names
            current_app.logger.info(f"Available sheets in {file.filename}: {sheet_names}")

            required_columns = ['ProjectName', 'CountyID', 'SourceOfFunds', 'FundingAmount']
            optional_columns = [
                'ImplementingAgency', 'Program', 'ConstituencyID', 'WardID', 'GPSCoordinates',
                'ProjectType', 'ProjectLocation', 'ScopeOfWorks', 'IntakeCapacity_m3',
                'TreatmentCapacity_m3', 'StorageCapacity_m3', 'TreatedWaterMains_km',
                'DistributionLines_km', 'NumberOfWaterKiosks', 'NumberOfConnections',
                'WastewaterCapacity_m3', 'TargetAreas', 'TargetBeneficiaries_Households',
                'TargetBeneficiaries_Population', 'Contractor', 'Consultant', 'StartDate',
                'PlannedEndDate', 'ActualEndDate', 'ProgressPercentage', 'TotalContractSum_KES',
                'CumulativeExpenditure_KES', 'OutstandingCost_KES', 'ExchequerReleases_KES',
                'SumOfPendingBills_KES', 'ApprovedBudgetFY2021_22', 'ApprovedBudgetFY2021_23',
                'ApprovedBudgetFY2022_23', 'ApprovedBudgetFY2022_24', 'ApprovedBudgetFY2023_24',
                'ApprovedBudgetFY2023_25', 'BudgetAllocationFY2024_25', 'BudgetAllocationFY2024_26',
                'ImpactsOfTheProject', 'KeyChallenges', 'Remarks'
            ]
            all_columns = required_columns + optional_columns

            if 'View Projects' in file.filename or any('View Projects' in sheet for sheet in sheet_names):
                flash(
                    f'It looks like you uploaded an export file ("{file.filename}") from the "View Projects" page. '
                    'Please upload a raw data file with columns: {", ".join(required_columns)}. '
                    'See example format in the upload instructions.', 
                    'danger'
                )
                return redirect(url_for('main.view_projects'))

            df = None
            for sheet in sheet_names:
                raw_df = pd.read_excel(
                    file,
                    engine='openpyxl' if file.filename.endswith('.xlsx') else 'xlrd',
                    sheet_name=sheet,
                    header=None,
                    nrows=5
                )
                raw_data = raw_df.to_string()
                current_app.logger.info(f"Raw data from sheet '{sheet}' (first 5 rows):\n{raw_data}")

                for header_row in range(5):
                    try:
                        temp_df = pd.read_excel(
                            file,
                            engine='openpyxl' if file.filename.endswith('.xlsx') else 'xlrd',
                            sheet_name=sheet,
                            header=header_row
                        )
                        temp_df.columns = temp_df.columns.str.strip()
                        current_app.logger.info(f"Sheet: {sheet}, Header row: {header_row}, Detected columns: {list(temp_df.columns)}")

                        excel_columns = [str(col).lower() for col in temp_df.columns]
                        required_columns_lower = [col.lower() for col in required_columns]
                        if all(col in excel_columns for col in required_columns_lower):
                            df = temp_df
                            break
                    except Exception as e:
                        current_app.logger.warning(f"Failed to read sheet {sheet} with header {header_row}: {str(e)}")
                if df is not None:
                    break

            if df is None:
                flash(
                    f'Could not find required columns {", ".join(required_columns)} in any sheet of "{file.filename}". '
                    'Ensure the file has a header row with these exact column names (case-insensitive) in the first 5 rows. '
                    'Check logs for detected columns and raw data.', 
                    'danger'
                )
                return redirect(url_for('main.view_projects'))

            column_map = {col: col.title() for col in df.columns}
            for req_col in required_columns + optional_columns:
                for orig_col in df.columns:
                    if str(orig_col).lower() == req_col.lower():
                        column_map[orig_col] = req_col
            df = df.rename(columns=column_map)

            df = df.fillna({
                col: '' for col in optional_columns if col in df.columns and 'Date' not in col
            }).fillna({
                col: None for col in optional_columns if col in df.columns and 'Date' in col
            })

            funding_map = {
                'GoK': 'GoK_KES', 'AFD': 'AFD_KES', 'ADB': 'ADB_KES', 'EU': 'EU_KES',
                'EIB': 'EIB_KES', 'KfW': 'KfW_KES', 'Belgium': 'Belgium_KES', 'Italy': 'Italy_KES',
                'Netherlands': 'Netherlands_KES', 'EXIMBank': 'EXIMBank_KES', 'WB': 'WB_KES',
                'BADEA': 'BADEA_KES', 'JICA': 'JICA_KES', 'KOREA': 'KOREA_KES', 'OFID': 'OFID_KES',
                'SAUDIARABIA': 'SAUDIARABIA_KES', 'DANIDA': 'DANIDA_KES'
            }

            for index, row in df.iterrows():
                def parse_date(date_val):
                    if pd.isna(date_val):
                        return None
                    try:
                        return pd.to_datetime(date_val).to_pydatetime()
                    except Exception:
                        return None

                new_project = Project(
                    **{col: row[col] for col in all_columns if col in df.columns and col not in ['SourceOfFunds', 'FundingAmount', 'StartDate', 'PlannedEndDate', 'ActualEndDate']},
                    StartDate=parse_date(row.get('StartDate')),
                    PlannedEndDate=parse_date(row.get('PlannedEndDate')),
                    ActualEndDate=parse_date(row.get('ActualEndDate'))
                )
                db.session.add(new_project)
                db.session.flush()  # Assigns auto-generated ProjectID

                source = row.get('SourceOfFunds', 'Unknown')
                amount = float(row.get('FundingAmount', 0)) if pd.notna(row.get('FundingAmount')) else 0
                if source in funding_map:
                    funding = Funding(
                        ProjectID=new_project.ProjectID,  # Use auto-generated ProjectID
                        SourceOfFunds=source,
                        **{funding_map[source]: amount}
                    )
                    db.session.add(funding)

            db.session.commit()
            flash('Projects uploaded successfully with auto-generated ProjectIDs!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading projects: {str(e)}', 'danger')
            current_app.logger.error(f"Upload error: {str(e)}", exc_info=True)

        return redirect(url_for('main.view_projects'))

    return render_template('upload_projects.html')



@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/protected')
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200