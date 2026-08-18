from flask import Flask, render_template, request, jsonify

import json
import random
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


app = Flask(__name__)


# ==========================================
# LOAD DATASET
# ==========================================

with open("intents.json", "r", encoding="utf-8") as file:

    data = json.load(file)


sentences = []
labels = []

responses = {}


for intent in data["intents"]:

    tag = intent["tag"]

    responses[tag] = intent["responses"]

    for pattern in intent["patterns"]:

        sentences.append(pattern)

        labels.append(tag)


# ==========================================
# TEXT VECTORIZATION
# ==========================================

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(sentences).toarray()


# ==========================================
# CREATE LABELS
# ==========================================

classes = sorted(list(set(labels)))

class_to_number = {
    tag: i
    for i, tag in enumerate(classes)
}


y = np.array([
    class_to_number[label]
    for label in labels
])


# ==========================================
# DEEP LEARNING MODEL
# ==========================================

model = Sequential([

    Dense(
        64,
        activation="relu",
        input_shape=(X.shape[1],)
    ),

    Dense(
        32,
        activation="relu"
    ),

    Dense(
        len(classes),
        activation="softmax"
    )

])


model.compile(

    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]

)


# ==========================================
# TRAIN MODEL AUTOMATICALLY
# ==========================================

print("\nTraining Deep Learning chatbot...\n")


model.fit(

    X,
    y,

    epochs=100,

    verbose=0

)


print("===================================")
print("CHATBOT MODEL TRAINED SUCCESSFULLY")
print("===================================\n")


# ==========================================
# CHATBOT FUNCTION
# ==========================================

def chatbot(message):

    user_vector = vectorizer.transform(
        [message]
    ).toarray()

    prediction = model.predict(
        user_vector,
        verbose=0
    )[0]

    predicted_index = np.argmax(prediction)

    confidence = prediction[predicted_index]

    if confidence < 0.40:

        return "Sorry, I don't understand. Please ask another question."


    predicted_tag = classes[predicted_index]

    return random.choice(
        responses[predicted_tag]
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# CHAT API
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "")

    response = chatbot(message)

    return jsonify({

        "response": response

    })


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )