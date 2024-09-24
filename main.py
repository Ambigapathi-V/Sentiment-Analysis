import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model
import streamlit as st

# Load the IMDB dataset's word index
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}

# Load the pretrained model with RELU activation
model = load_model('simple_rnn_imbd.h5')

# Step 2: Helper Functions

def decode_review(encoded_review):
    """Decode a review from its encoded representation."""
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

def preprocess_text(text):
    """Preprocess the user input text for prediction."""
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]
    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review

def predict_sentiment(review):
    """Predict the sentiment of a given review."""
    preprocessed_input = preprocess_text(review)
    prediction = model.predict(preprocessed_input)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment, prediction[0][0]

# Streamlit app UI enhancements
st.title('IMDB Movie Review Sentiment Analysis')
#st.image('https://image.shutterstock.com/image-vector/movie-review-icon-isolated-on-260nw-1390851956.jpg', width=300)  # Replace with your own image URL
st.write('**Enter a movie review to classify it as positive or negative.**')

# User Input
user_input = st.text_area('Movie Review', height=150)

if st.button('Classify'):
    with st.spinner('Classifying...'):
        # Make Prediction
        prediction = model.predict(preprocess_text(user_input))
        sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
        
        # Display the Result
        st.success(f'Sentiment: **{sentiment}**')
        st.write(f'Probability: **{prediction[0][0]:.4f}**')
else:
    st.warning('Please click the button to classify the review')
