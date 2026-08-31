import pandas as pd
import numpy as np

data = pd.read_excel(
    "D:\\pythoncoding\\Final_year_project\\Patient flow and Disease trend A case study of Medical Department DHQ hospital Timergara.xlsx"
)

# =====================================================
# Clean Type_of_Discharge Column
# =====================================================

data['Type_of_Discharge'] = (
    data['Type_of_Discharge']
    .astype(str)
    .str.strip()
    .str.upper()
)

# =====================================================
# Standard Mapping Rules
# =====================================================

replacement_map = {

    'DEATH': 'DEATH',
    'DEA.': 'DEATH',
    'DEAD': 'DEATH',

    'LAMA': 'LAMA',
    'LEFT AGAINST MEDICAL ADVICE': 'LAMA',
    'LEFT AGAINST MEDICAL ADVICE.': 'LAMA',

    'REFFERED': 'REFERRED',
    'REFERED': 'REFERRED',
    'REFFERED.': 'REFERRED',

    'SHIFT TO CCU': 'DOR',
    'SHIFTED TO CCU': 'DOR',

    'TRUE': 'DOR',

    'NAN': 'DOR',
    'NONE': 'DOR',
    '': 'DOR',

    'ANY OPERATION PROCEDURE DONE': 'DOR',
    'OPERATION DONE': 'DOR',
    'PROCEDURE DONE': 'DOR'

}

# =====================================================
# Apply Mapping
# =====================================================

data['Type_of_Discharge'] = (
    data['Type_of_Discharge']
    .replace(replacement_map)
)

# =====================================================
# Final Safety Clean (unknown values → DOR)
# =====================================================

valid_types = ['DEATH', 'REFERRED', 'DOR', 'RECOVERED', 'DISCHARGED', 'IMPROVED','LAMA']

data['Type_of_Discharge'] = np.where(

    data['Type_of_Discharge'].isin(valid_types),
    data['Type_of_Discharge'],
    'DOR'

)

# =====================================================
# Final Check
# =====================================================

print(data['Type_of_Discharge'].value_counts())
data.to_excel("Patient flow and Disease trend A case study of Medical Department DHQ hospital Timergara.xlsx" ,index=False)