import numpy as np
import pandas as pd
from scipy.optimize import fmin_cg

# Load the dataset (replace with the path to your dataset)
df = pd.read_csv('./cosmetics.csv')

# Simulate user-item interaction data (replace with actual data)
# For demonstration, we create a matrix of random ratings
num_users = 100  # Example number of users
num_products = df.shape[0]
ratings = np.random.rand(num_products, num_users)

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

# Save the predicted ratings to a file
np.save('predicted_ratings.npy', predicted_ratings)

print("Predicted ratings saved to 'predicted_ratings.npy'")
