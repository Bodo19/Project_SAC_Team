import numpy as np
import pandas as pd
from scipy.optimize import fmin_cg

# Load the dataset
df = pd.read_csv('./cosmetics.csv')

# Simulated user-item interaction data. Replace with actual data
# Here we simulate both the ratings and user selections
num_users = 100  # Example number of users
num_products = df.shape[0]

# Simulate initial random ratings
ratings = np.random.rand(num_products, num_users)

# Load user selections data from your storage system
# The loading mechanism depends on how you store this data (e.g., database, file)
user_selections = load_user_selections()  # This should return a matrix similar to your hardcoded example


# Simulate user preferences - replace with your actual user preference data
# For simplicity, using random skin types
user_preferences = np.random.choice(['Combination', 'Dry', 'Normal', 'Oily'], num_users)

# Adjust ratings based on user selections
selection_weight = 2  # Weight to add for each user selection
ratings += (user_selections * selection_weight)

# Adjust ratings based on user preferences
for i, skin_type in enumerate(user_preferences):
    suitable_products = df[skin_type] == 1
    ratings[:, i] += (suitable_products * selection_weight)

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
args=(norm_ratings, num_users, num_products, num_features, lambda_reg),maxiter=100)

X_opt = result[:num_products * num_features].reshape(num_products, num_features)
Theta_opt = result[num_products * num_features:].reshape(num_users, num_features)

predicted_ratings = X_opt @ Theta_opt.T + mean_ratings[:, np.newaxis]

np.save('predicted_ratings.npy', predicted_ratings)

print("Predicted ratings saved to 'predicted_ratings.npy'")