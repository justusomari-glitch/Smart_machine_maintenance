#creating schemas for each model based on the features in that model
from pydantic import BaseModel
import joblib

failure_model = joblib.load('models/failure_detection.pkl')
maintenance_model = joblib.load('models/maintenance_prediction.pkl')
days_model = joblib.load('models/daysto_next_failure.pkl')


print("Failure Features:", failure_model.feature_names_in_)
print("Maintenance Features:", maintenance_model.feature_names_in_)
print("Days Features:", days_model.feature_names_in_)




class FailureDetectionSchema(BaseModel):
    vibration_mm_s: float
    temperature_c: float
    load_percent: float
    motor_current_amp: float
    plant_section: str
    component: str
    sub_equipment: str
    major_equipment: str

class MaintenancePredictionSchema(BaseModel):
    plant_section: str
    major_equipment: str
    sub_equipment: str
    component: str
    root_cause_category: str
    operating_hours: float
    load_percent: float
    vibration_mm_s: float
    temperature_c: float
    motor_current_amp: float
    recommended_shelf_life_days: int
    days_to_next_failure: float

class DaysToNextFailureSchema(BaseModel):
    component: str
    sub_equipment: str
    major_equipment: str
    plant_section: str
    maintenance_type: str
    vibration_mm_s: float
    temperature_c: float
    load_percent: float
    motor_current_amp: float
    operating_hours: float