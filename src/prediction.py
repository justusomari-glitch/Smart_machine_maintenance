import pandas as pd
import joblib
from pydantic import BaseModel
from fastapi import FastAPI
from src.schema import FailureDetectionSchema, MaintenancePredictionSchema, DaysToNextFailureSchema

app = FastAPI(title="Smart Machine Maintenance API", description="API for predicting machine failure, maintenance needs, and days to next failure",)

# Load the models
failure_model = joblib.load('models/failure_detection.pkl')
maintenance_model = joblib.load('models/new_maintenance.pkl') 
days_model = joblib.load('models/new_duration.pkl')
threshold = joblib.load('models/threshold.pkl')

print("Models loaded successfully")
print("Threshold loaded successfully:", threshold)

FAILURE_FEATURES = [
    "vibration_mm_s",
    "temperature_c",
    "load_percent",
    "motor_current_amp",
    "plant_section",
    "component",
    "sub_equipment",
    "major_equipment"
]

MAINTENANCE_FEATURES =[
    "plant_section",
    "major_equipment",
    "sub_equipment",
    "component",
    "operating_hours",
    "load_percent",
    "vibration_mm_s",
    "temperature_c",
    "motor_current_amp",
    
]

DAYS_FEATURES = [
    "component",
    "sub_equipment",
    "major_equipment",
    "plant_section",
    "vibration_mm_s",
    "temperature_c",
    "load_percent",
    "motor_current_amp",
    "operating_hours"
]

class CombinedInputSchema(BaseModel):
    vibration_mm_s: float
    temperature_c: float
    load_percent: float
    motor_current_amp: float
    plant_section: str
    component: str
    sub_equipment: str
    major_equipment: str
    operating_hours: float
    

def make_df(data:dict,columns:list)->pd.DataFrame:
   return pd.DataFrame([{col :data[col] for col in columns}])

@app.get("/")
def home():
    return {"message": "Welcome to the Smart Machine Maintenance API. Use the /predict endpoint to get predictions."}

@app.post("/predict")
def predict_all(payload: CombinedInputSchema):
    data=payload.model_dump()
    failure_df = make_df(data, FAILURE_FEATURES)
    failure_probability =failure_model.predict_proba(failure_df)[0][1]
    failure_prediction = int(failure_probability >= threshold)
    maintenance_df = make_df(data, MAINTENANCE_FEATURES)
    maintenance_prediction = maintenance_model.predict(maintenance_df)[0]
    days_df = make_df(data, DAYS_FEATURES)
    days_to_next_failure = float(days_model.predict(days_df)[0])
    days_to_next_failure = max(days_to_next_failure, 0)

    if failure_prediction == 1 or days_to_next_failure <= 3:
        failure_message = "Machine Failure Imminent"
        status = "Critical - Immediate Action Required"
    elif failure_prediction == 1 or days_to_next_failure <= 7:
        failure_message = "Machine Failure Likely"
        status = "High Risk of Failure"
    else:
        failure_message = "No Imminent Failure Detected"
        status = "Normal Operation"
    return {
        "failure_message": failure_message,
        "failure_probability": round(failure_probability, 2),
        "maintenance_type": maintenance_prediction,
        "days_to_next_failure": round(days_to_next_failure, 2),
        "status": status
    }