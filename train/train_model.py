import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import joblib

def train_model():
    # Load data
    df = pd.read_csv("data/train.csv")

    # Define Scaler
    con_transformer = Pipeline(steps=[('robust', RobustScaler())])
    cat_transformer = Pipeline(steps=[('onehot', OneHotEncoder())])

    # Define features and target
    cat_cols = ['sex','exng','caa','cp','slp','thall']
    con_cols = ["age","thalachh","oldpeak"]

    # Drop unnecessary columns
    x = df.drop(columns=['output',"chol","trtbps","fbs",'restecg'])

    preprocessor = ColumnTransformer(
        remainder='passthrough', #passthough features not listed
        transformers=[
            ('rob', con_transformer , con_cols),
            ('onehot', cat_transformer , cat_cols)
        ])

    pipe = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', SVC(C=7, gamma=0.1 ,random_state=42))])

    # Define target
    y = df['output']

    # Fit model
    pipe.fit(x, y)

    # Save model
    joblib.dump(pipe, "src/svm_model.joblib")



if __name__ == "__main__":
    train_model()