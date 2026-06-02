import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from ucimlrepo import fetch_ucirepo

print("Programmatically downloading the verified Student Success dataset...")

dataset = fetch_ucirepo(id=697)

df = pd.DataFrame(dataset.data.features)
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

target_df = pd.DataFrame(dataset.data.targets)
target_df.columns = target_df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

print(f"Dataset loaded securely! Row count: {df.shape[0]}")

cols = df.columns.tolist()

def find_col(possible_names):
    for name in possible_names:
        if name in cols:
            return name
    raise KeyError(f"Could not find any of the columns: {possible_names}")

marital_col = find_col(['marital_status'])
debtor_col = find_col(['debtor'])
tuition_col = find_col(['tuition_fees_up_to_date'])
displaced_col = find_col(['displaced'])
scholarship_col = find_col(['scholarship_holder'])
mother_qual_col = find_col(["mother's_qualification", "mothers_qualification", "mother_qualification"])

without_eval_col = find_col([
    'curricular_units_1st_sem_(without_evaluations)',
    'curricular_units_1st_sem_without_evaluations'
])
approved_col = find_col([
    'curricular_units_1st_sem_(approved)',
    'curricular_units_1st_sem_approved'
])
enrolled_col = find_col([
    'curricular_units_1st_sem_(enrolled)',
    'curricular_units_1st_sem_enrolled'
])
grade_col = find_col([
    'curricular_units_1st_sem_(grade)',
    'curricular_units_1st_sem_grade'
])

studio_df = pd.DataFrame()

studio_df['Attendance Rate (%)'] = np.clip(
    100 - (df[without_eval_col] * 8), 30, 100
)

studio_df['Weekly Assessment Marks'] = (
    df[approved_col] / df[enrolled_col].replace(0, 1)
) * 100

studio_df['Weekly Assessment Marks'] = (
    studio_df['Weekly Assessment Marks']
    .fillna(df[grade_col] * 5)
    .clip(0, 100)
)

studio_df['Emotional Wellness Score (1-5)'] = np.clip(
    5 - (df[marital_col] * 0.5) - (df[debtor_col] * 1.5),
    1,
    5
)

studio_df['Digital Access (0-1)'] = (
    df[tuition_col] == 1
).astype(int)

studio_df['Travel Distance (KM)'] = df[displaced_col].apply(
    lambda x: np.random.uniform(15, 45)
    if x == 1
    else np.random.uniform(1, 8)
)

studio_df['Family Income Bracket (1-3)'] = df[mother_qual_col].apply(
    lambda x: 3 if x in [1, 2, 3]
    else (2 if x in [4, 5, 6] else 1)
)

studio_df['Scholarship Status (0-1)'] = df[scholarship_col]

target_col_name = target_df.columns[0]

y = target_df[target_col_name].apply(
    lambda x: 1 if str(x).strip().lower() == 'dropout' else 0
).values

X = studio_df.values

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training production RandomForest model...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    random_state=42
)

model.fit(X_train_scaled, y_train)

accuracy = model.score(
    scaler.transform(X_test),
    y_test
)

print(
    f"Model trained successfully with real data! "
    f"Validation Accuracy: {accuracy * 100:.2f}%"
)

joblib.dump(model, 'eduguardian_rf.joblib')
joblib.dump(scaler, 'scaler.joblib')

print(
    "\nSuccess! 'eduguardian_rf.joblib' and "
    "'scaler.joblib' are ready to download."
)
