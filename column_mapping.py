COLUMN_CATEGORIES = {
    'employee_info': {
        'description': 'Core employee identification and basic information',
        'columns': [
            'Employee Code', 'Employee Name', 'Gender', 'Level', 'Designation',
            'Employment Status', 'Nature Of Employment', 'Date of Joining',
            'Total Experience', 'Email ID', 'Mobile Number', 'Visa'
        ],
        'key_metrics': ['headcount', 'experience_distribution', 'level_distribution']
    },
    
    'location_info': {
        'description': 'Geographic and work arrangement details',
        'columns': [
            'Location', 'Base Location', 'State', 'Region', 'Work Mode'
        ],
        'key_metrics': ['location_distribution', 'remote_vs_office', 'regional_analysis']
    },
    
    'project_allocation': {
        'description': 'Current and historical project assignment information',
        'columns': [
            'Client Name', 'Project Name', 'Project Department', 'Project Type',
            'Actual Allocation Start Date', 'Expected Billing Start Date',
            'Allocation Start Date', 'Allocation End Date', 'Loading Percentage',
            'Planned ReleaseDate', 'SOW Role', 'Primary Ro', 'ADM', 'PMO Name'
        ],
        'key_metrics': ['allocation_rate', 'loading_efficiency', 'client_distribution', 'project_duration']
    },
    
    'skills_training': {
        'description': 'Technical skills, certifications, and training programs',
        'columns': [
            'Tech1 Primary Skill', 'Tech1 NonPrimary Skill', 'Tech2 Primary Skill',
            'Tech2 NonPrimary Skill', 'Training Plan', 'Training Need Identified',
            'Tech1 For Training', 'Tech 2 For Training', 'Training Status',
            'Certifications', 'Skill', 'Last Skill Update on'
        ],
        'key_metrics': ['skill_inventory', 'training_completion', 'certification_status', 'skill_gaps']
    },
    
    'bench_management': {
        'description': 'Bench status, ageing, and management tracking',
        'columns': [
            'Status', 'Bench Category', 'Reason For Bench', 'Current Ageing',
            'Actual Ageing', 'Current Ageing Slab', 'Actual Ageing Slab',
            'Current Ageing Slab Sort', 'Actual Ageing Slab Sort',
            'Bench Ageing >8Wks Reason', 'Bench Ageing >8Wks Remarks'
        ],
        'key_metrics': ['bench_percentage', 'average_ageing', 'ageing_distribution', 'bench_reasons']
    },
    
    'workforce_planning': {
        'description': 'Future planning and workforce management',
        'columns': [
            'BU Owner', 'WFM Owner Name', 'WFM Plan Status', 'WFM Plan Date',
            'Expected Allocation Start Date', 'Expected Client Name',
            'Expected Project Name', 'Available for Other BU', 'WFM Capability Input',
            'Deployment Remarks'
        ],
        'key_metrics': ['planning_accuracy', 'cross_bu_availability', 'deployment_timeline']
    },
    
    'performance_metrics': {
        'description': 'Performance evaluations and ratings',
        'columns': [
            'Associate RAG Status', 'SME Evaluation', 'Evaluation Tool',
            'Evaluation Tool/Training Remarks', 'No Of Evaluation',
            'Last Evaluation Reason', 'ATL Eligible', 'ATL Remarks',
            'Associate Classification'
        ],
        'key_metrics': ['rag_distribution', 'evaluation_scores', 'atl_eligibility']
    },
    
    'hr_admin': {
        'description': 'HR administrative and compliance information',
        'columns': [
            'HRBP', 'BGV Status', 'BGV Closure Status', 'Expected BGV Closure Date',
            'Contract EndDate', 'Notice Period', 'Offer Type', 'LOB',
            'MITy', 'Load'
        ],
        'key_metrics': ['bgv_compliance', 'contract_expiry', 'notice_period_analysis']
    },
    
    'separation_info': {
        'description': 'Employee separation and exit information',
        'columns': [
            'Date Of Resignation', 'Last Working Day', 'Nature Of Separation',
            'Reason', 'Primary Reason', 'Resignation Status', 'Last Release Reason',
            'Released Feedback'
        ],
        'key_metrics': ['attrition_rate', 'separation_reasons', 'exit_feedback']
    },
    
    'historical_tracking': {
        'description': 'Historical data and tracking information',
        'columns': [
            'Last Project Release Date', 'Last BU Released From', 'Last Client Released From',
            'Last Project Released From', 'First On-Boarding Date', 'First Project Allocation Date',
            'First Billing Date', 'Previous Status', 'Hired_Released', 'Hired_Released Month'
        ],
        'key_metrics': ['tenure_analysis', 'project_history', 'allocation_patterns']
    },
    
    'leave_management': {
        'description': 'Leave and absence tracking',
        'columns': [
            'Leave Status', 'Leave Type', 'Leave Start Date', 'Leave End Date'
        ],
        'key_metrics': ['leave_utilization', 'absence_patterns']
    },
    
    'recruitment_onboarding': {
        'description': 'Recruitment and onboarding process tracking',
        'columns': [
            'Interview Panel Member', 'CV Available', 'CV Uploaded By', 'CV Uploaded Date',
            'Allocated On SF ID', 'SF ID Hired For', 'BU Hired For', 'Client Hired For',
            'Project Hired For', 'Opportunity ID', 'Greeting Mail Sent'
        ],
        'key_metrics': ['onboarding_efficiency', 'recruitment_pipeline']
    },
    
    'system_tracking': {
        'description': 'System and process tracking fields',
        'columns': [
            'Last Modified By', 'Last Modified On', 'Status SubType', 'Allocation Remark',
            'Resource Remarks', 'Replacement Required', 'Allocation Req ID',
            'SupportingDocuments'
        ],
        'key_metrics': ['data_freshness', 'process_compliance']
    }
}

def get_all_columns():
    all_columns = []
    for category in COLUMN_CATEGORIES.values():
        all_columns.extend(category['columns'])
    return all_columns

def get_category_for_column(column_name):
    for category_name, category_info in COLUMN_CATEGORIES.items():
        if column_name in category_info['columns']:
            return category_name
    return 'uncategorized'

def get_missing_columns(df_columns):
    all_expected = get_all_columns()
    return [col for col in all_expected if col not in df_columns]

def get_extra_columns(df_columns):
    all_expected = get_all_columns()
    return [col for col in df_columns if col not in all_expected]
