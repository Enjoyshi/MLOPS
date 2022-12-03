import joblib
import pandas as pd

def test_model():
    # Load model
    pipe = joblib.load("train/svm_model.joblib")

    # Load data
    df = pd.read_csv("data/test.csv")

    # Define features and target
    y = df['output']
    x = df.drop(columns=['output',"chol","trtbps","fbs",'restecg'])

    # Evaluate model
    score = pipe.score(x, y)
    print("Model accuracy: ", score)

if __name__ == "__main__":
    test_model()

