import pydantic
from fastapi import FastAPI
import pandas as pd
import joblib
import numpy as np
import uvicorn


app = FastAPI()

model_path = "model/xgboost_best_model.pkl"
load_model = joblib.load(model_path)


class HouseFeatures(pydantic.BaseModel):
    Bedrooms:float
    Bathrooms: float
    luxuryFeatures: int
    comfortFeatures :int
    utilityFeatures : int
    connectivityFeatures :int
    exSpace: int


@app.post("/predict_price")

def predict_house_price(features : HouseFeatures):
    input_data_as_dict = features.model_dump()
    input_df = pd.DataFrame([input_data_as_dict])

    prediction = load_model.predict(input_df)

    actual_price = float(np.exp(prediction[0]))


    return {"Predicted_price": actual_price}


@app.get("/")
def read_root():
    return {"message":"Ml model API is running"}


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port = 8000)