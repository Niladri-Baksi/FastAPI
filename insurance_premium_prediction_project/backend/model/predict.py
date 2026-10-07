import pickle
import pandas as pd

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)


MODEL_VERSION = "1.0.0"  # Define the model version manually but generally extracted from MLflow.

#get class labels from the model(imp for matching probabilities with class labels)
class_labels = model.classes_.tolist()  # Convert numpy array to list

# def predict_output(user_input: dict):
#     # Convert the user data to a DataFrame
#     input_df = pd.DataFrame([user_input])

#     output=model.predict(input_df)[0] #output in list, since model.predict() is designed for multiple rows or batch predictions so getting the 1st element is viable here since we are only predicting for a single row of data. But for single row [0] is optional.
#     return output


#polished version of the above function 
def predict_output(user_input: dict):
    # Convert the user data to a DataFrame
    input_df = pd.DataFrame([user_input])

    #predict the class
    predicted_class = model.predict(input_df)[0]  # Get the predicted class for the input data

    # Get the predicted probabilities for each class
    probabilities = model.predict_proba(input_df)[0]  #Get the first (and only) row of probabilities
    confidence=max(probabilities)  # Get the maximum probability as confidence score

    #create mappung -- {class_label: probability}
    class_probs=dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))  # Round probabilities to 4 decimal places for better readability

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),  # Round confidence to 4 decimal places
        "class_probabilities": class_probs
    }


        