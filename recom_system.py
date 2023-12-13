import numpy as np
import pandas as pd
from scipy.optimize import fmin_cg
import random

# Simulated function to get user skin type - to be replaced with actual user data
def get_user_skin_type(user_id):
    # This should be replaced with a function that returns the user's skin type
    return np.random.choice(['Combination', 'Dry', 'Normal', 'Oily'])

# Load the dataset (replace with the path to your dataset)
df = pd.read_csv('./cosmetics.csv')

# Simulate user-item interaction data (replace with actual data)
# For demonstration, we create a matrix of random ratings
num_users = 100  # Example number of users
num_products = df.shape[0]
ratings = np.random.rand(num_products, num_users)

# Users' skin types (randomly assigned for demonstration)
user_skin_types = [get_user_skin_type(i) for i in range(num_users)]

# Normalize ratings
def normalize_ratings(ratings):
    mean_ratings = np.nanmean(ratings, axis=1)
    ratings_diff = ratings - mean_ratings[:, np.newaxis]
    return ratings_diff, mean_ratings

norm_ratings, mean_ratings = normalize_ratings(ratings)

# Collaborative Filtering
def cost_function(params, Y, num_users, num_products, num_features, lambda_reg):
    X = params[:num_products*num_features].reshape(num_products, num_features)
    Theta = params[num_products*num_features:].reshape(num_users, num_features)
    
    prediction_error = (X @ Theta.T - Y)
    cost = 0.5 * np.nansum(prediction_error**2)
    cost += (lambda_reg / 2) * (np.sum(Theta**2) + np.sum(X**2))
    return cost

def gradient(params, Y, num_users, num_products, num_features, lambda_reg):
    X = params[:num_products*num_features].reshape(num_products, num_features)
    Theta = params[num_products*num_features:].reshape(num_users, num_features)
    
    prediction_error = (X @ Theta.T - Y)
    X_grad = prediction_error @ Theta + lambda_reg * X
    Theta_grad = prediction_error.T @ X + lambda_reg * Theta
    
    return np.hstack((X_grad.ravel(), Theta_grad.ravel()))

# Optimization
num_features = 10
X = np.random.rand(num_products, num_features)
Theta = np.random.rand(num_users, num_features)
initial_params = np.hstack((X.ravel(), Theta.ravel()))
lambda_reg = 10

result = fmin_cg(cost_function, initial_params, fprime=gradient,
                 args=(norm_ratings, num_users, num_products, num_features, lambda_reg),
                 maxiter=100)

# Extract optimized X and Theta
X_opt = result[:num_products*num_features].reshape(num_products, num_features)
Theta_opt = result[num_products*num_features:].reshape(num_users, num_features)

# Making Predictions
predicted_ratings = X_opt @ Theta_opt.T + mean_ratings[:, np.newaxis]

# Recommendation function
def recommend_products(user_id, predicted_ratings, user_skin_type, df):
    user_ratings = predicted_ratings[:, user_id]
    product_indices = np.argsort(user_ratings)[::-1]  # Sort product indices based on predicted rating
    
    recommended_products = []
    top_n = random.randint(10, 15)  # Randomly select between 10 and 15 recommendations

    for product_idx in product_indices:
        product = df.iloc[product_idx]
        if product[user_skin_type]:
            # Include skin type information with the product name
            suitable_for = [skin for skin in ['Combination', 'Dry', 'Normal', 'Oily'] if product[skin]]
            recommended_products.append((product['Name'], ', '.join(suitable_for)))
            if len(recommended_products) >= top_n:
                break
                
    return recommended_products

# Example usage
user_id = 0  # Example user ID
user_skin_type = user_skin_types[user_id]
recommended = recommend_products(user_id, predicted_ratings, user_skin_type, df)
print("Recommended Products:", recommended)
