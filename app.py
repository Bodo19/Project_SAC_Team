from flask import Flask, redirect, render_template, request, session, url_for
import numpy as np
import pandas as pd
import os
import random
from flask import jsonify

# Assuming your recommendation script is in a file named 'recommender.py'
from recom_system import recommend_products

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # In a real application, you would verify username and password here
        username = request.form.get('username')
        session['username'] = username  # Store username in session
        return redirect(url_for('index'))
    return render_template('login.html')

# Modified Index Route to include session and user actions
def increment_user_id(user_id):
    # Implement logic to increment the user ID
    # For example, retrieve the current user ID from a database or file and increment it
    return user_id + 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        user_skin_type = request.form.get('skin_type')
        user_id = increment_user_id(user_id)  # Increment the user ID
        predicted_ratings = np.load('./predicted_ratings.npy')
        
        recommended = recommend_products(user_id, predicted_ratings, user_skin_type, cosmetics)
        return render_template('recommendations.html', recommendations=recommended, skin_type=user_skin_type, user_id=user_id)
    return render_template('index.html')

# Add a route for item selection
@app.route('/select-item/<int:product_id>')
def select_item(product_id):
    # Implement logic to store user's item selection, possibly in a database or file
    # For example, appending to a file:
    with open('user_actions.txt', 'a') as file:
        file.write(f"{session['username']} selected item {product_id}\n")
    return redirect(url_for('item_details', product_id=product_id))

# Route for displaying item details
@app.route('/products/<int:product_id>')
def item_details(product_id):
    try:
        item = get_item_details(product_id)
        recommendations = get_recommendations(product_id)  # Get recommendations based on the item
        return render_template('item_details.html', item=item, recommendations=recommendations)
    except IndexError:
        return "Item not found", 404

@app.route('/api/products')
def api_products():
    products = get_products_data()
    return jsonify(products)

@app.route('/api/products/<int:index>')
def api_product_details(index):
    try:
        product_details = get_item_details(index)
        return jsonify(product_details)
    except IndexError:
        return jsonify({"error": "Product not found"}), 404

def get_products_data():
    # Read the cosmetics CSV file into a DataFrame
    cosmetics_df = pd.read_csv('./cosmetics.csv')
    # Convert DataFrame to a list of dictionaries
    products_data = cosmetics_df.to_dict(orient='records')
    return products_data

# Implement get_item_details to fetch details based on DataFrame index
def get_item_details(index):
    cosmetics_df = pd.read_csv('./cosmetics.csv')
    product_details = cosmetics_df.iloc[index].to_dict()
    return product_details

@app.route('/api/recommendations/<int:product_id>')
def api_recommendations(product_id):
    recommendations = get_recommendations(product_id)
    return jsonify(recommendations)

def get_recommendations(product_id):
    cosmetics_df = pd.read_csv('./cosmetics.csv')
    # Simple example: return 5 random products as recommendations
    recommendations = cosmetics_df.sample(5).to_dict(orient='records')
    return recommendations

@app.route('/api/products/<int:index>', methods=['POST'])
def save_selections():
    data = request.json
    # Process and save this data
    # You might save it to a database or a file
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
