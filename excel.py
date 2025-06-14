import pandas as pd

# Data dictionary with all columns
data = {
    "ProjectID": [1, 2],
    "ProjectName": ["Water Supply Project", "Sewer Upgrade"],
    "CountyID": [1, 2],
    "SourceOfFunds": ["GoK", "AFD"],
    "FundingAmount": [5000000, 8000000],
    "ImplementingAgency": ["Water Board", "Sanitation Dept"],
    "Program": ["Rural Water", "Urban Sanitation"],
    "ConstituencyID": [1, 2],
    "WardID": [1, 2],
    "GPSCoordinates": ["-1.2921, 36.8219", "-1.9432, 36.1234"],
    "ProjectType": ["Water Supply", "Sanitation"],
    "ProjectLocation": ["Nairobi", "Mombasa"],
    "ScopeOfWorks": ["Install pipes and tanks", "Upgrade sewer lines"],
    "IntakeCapacity_m3": [1000, 0],
    "TreatmentCapacity_m3": [800, 0],
    "StorageCapacity_m3": [1200, 0],
    "TreatedWaterMains_km": [10, 0],
    "DistributionLines_km": [15, 20],
    "NumberOfWaterKiosks": [5, 0],
    "NumberOfConnections": [200, 0],
    "WastewaterCapacity_m3": [500, 1500],
    "TargetAreas": ["Urban slums", "Coastal towns"],
    "TargetBeneficiaries_Households": [1000, 1500],
    "TargetBeneficiaries_Population": [5000, 7500],
    "Contractor": ["ABC Contractors", "DEF Builders"],
    "Consultant": ["XYZ Consultants", "GHI Advisors"],
    "StartDate": ["2023-01-01", "2023-06-01"],
    "PlannedEndDate": ["2024-12-31", "2025-06-30"],
    "ActualEndDate": ["", ""],
    "ProgressPercentage": [75, 50],
    "TotalContractSum_KES": [10000000, 12000000],
    "CumulativeExpenditure_KES": [7500000, 6000000],
    "OutstandingCost_KES": [2500000, 6000000],
    "ExchequerReleases_KES": [6000000, 5000000],
    "SumOfPendingBills_KES": [1500000, 2000000],
    "ApprovedBudgetFY2021_22": [2000000, 3000000],
    "ApprovedBudgetFY2021_23": [2500000, 3500000],
    "ApprovedBudgetFY2022_23": [3000000, 4000000],
    "ApprovedBudgetFY2022_24": [3500000, 4500000],
    "ApprovedBudgetFY2023_24": [4000000, 5000000],
    "ApprovedBudgetFY2023_25": [4500000, 5500000],
    "BudgetAllocationFY2024_25": [5000000, 6000000],
    "BudgetAllocationFY2024_26": [5500000, 6500000],
    "ImpactsOfTheProject": ["Improved water access", "Better sanitation"],
    "KeyChallenges": ["Funding delays", "Weather issues"],
    "Remarks": ["On track", "Needs review"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file
df.to_excel("projects_data.xlsx", index=False)

print("Excel file 'projects_data.xlsx' has been generated in your current directory.")