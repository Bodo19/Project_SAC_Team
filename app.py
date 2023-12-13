from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import os
import random

# Assuming your recommendation script is in a file named 'recommender.py'
from recom_system import recommend_products

app = Flask(__name__)

cosmetics = pd.read_csv('./cosmetics.csv')

import random

def recommend_products(user_id, predicted_ratings, user_skin_type, df):
    user_ratings = predicted_ratings[:, user_id]
    product_indices = np.argsort(user_ratings)[::-1]  # Sort product indices based on predicted rating
    
    recommended_products = []
    top_n = random.randint(10, 15)  # Choose a random number between 10 and 15 for the number of recommendations

    for product_idx in product_indices:
        product = df.iloc[product_idx]
        if product[user_skin_type]:
            suitable_for = ', '.join([skin for skin in ['Combination', 'Dry', 'Normal', 'Oily'] if product[skin]])
            recommended_products.append((product['Name'], suitable_for))
            if len(recommended_products) >= top_n:
                break
                
    return recommended_products

def get_last_user_id():
    if os.path.exists('last_user_id.txt'):
        with open('last_user_id.txt', 'r') as file:
            last_id = file.read()
            return int(last_id)
    else:
        return 0

# Function to increment and save the new user ID
def increment_user_id():
    new_id = get_last_user_id() + 1
    with open('last_user_id.txt', 'w') as file:
        file.write(str(new_id))
    return new_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_skin_type = request.form.get('skin_type')
        user_id = increment_user_id()  # Increment the user ID
        
        predicted_ratings = np.load('./predicted_ratings.npy')
        
        recommended = recommend_products(user_id, predicted_ratings, user_skin_type, cosmetics)
        return render_template('recommendations.html', recommendations=recommended, skin_type=user_skin_type)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
