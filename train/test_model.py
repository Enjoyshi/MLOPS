import joblib
import pandas as pd
import matplotlib.pyplot as plt

def test_model():
    # Load model
    pipe = joblib.load("src/svm_model.joblib")

    # Load data
    df = pd.read_csv("data/test.csv")

    # Define features and target
    y = df['output']
    x = df.drop(columns=['output',"chol","trtbps","fbs",'restecg'])

    # Evaluate model
    score = pipe.score(x, y)
    print("Model accuracy: ", score)

    # Recall
    y_pred = pipe.predict(x)
    from sklearn.metrics import recall_score
    recall = recall_score(y, y_pred)
    print("Recall: ", recall)

    # Precision
    from sklearn.metrics import precision_score
    precision = precision_score(y, y_pred)
    print("Precision: ", precision)

    #Save the confusion matrix
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y, y_pred)
    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('train/img/confusion_matrix.png')

if __name__ == "__main__":
    test_model()

