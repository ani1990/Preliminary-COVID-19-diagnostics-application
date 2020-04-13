import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
#from keras.models import load_model
import librosa 
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Encode the classification labels
le = LabelEncoder()

def extract_feature(file_name):
   
    try:
        audio_data, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)
        print("Gkiri-1:extrct feature done ", file_name)        
    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None, None

    return np.array([mfccsscaled])

def print_prediction(file_name):
    prediction_feature = extract_feature(file_name)
    
    #Load pre trained model
    model = load_model("/home/ubuntu/flaskapp2/weights.best.basic_mlp.hdf5")
    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    print("The predicted class is:", predicted_class[0], '\n')

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)):
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )


def print_prediction_simple(file_name):
    prediction_feature = extract_feature(file_name)

    #Load pre trained model
    #model = load_model("weights.best.basic_mlp.hdf5")
    model = load_model("/home/ubuntu/flaskapp2/weights.best.basic_mlp.hdf5")

    predicted_vector = model.predict_classes(prediction_feature)
    print("The predicted class is:", predicted_vector[0], '\n')
    

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)):
        print("\t\t : ", format(predicted_proba[i], '.32f') )

    
    #return predicted_vector[0]
    return predicted_proba

#filename = 'cough2.wav' 
#print_prediction_simple(filename)
