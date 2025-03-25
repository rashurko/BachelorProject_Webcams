import numpy as np
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
from scipy.stats import t

def linear_regression(x_values, y_values, output_folder, confidence=0.95):
    # Convert the lists to numpy arrays
    x_values = np.array(x_values)
    y_values = np.array(y_values)
    
    # Add a constant to the x values for the intercept
    x_with_const = sm.add_constant(x_values)
    
    # Perform linear regression on the data
    model = sm.OLS(y_values, x_with_const).fit()
    slope = model.params[1]
    intercept = model.params[0]
    slope_std_err = model.bse[1]
    intercept_std_err = model.bse[0]
    r_squared = model.rsquared
    
    # Print the regression results
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"R-squared: {r_squared}")
    print(f"Slope Standard Error: {slope_std_err}")
    print(f"Intercept Standard Error: {intercept_std_err}")
    
    # Calculate the confidence intervals
    n = len(x_values)
    t_value = t.ppf((1 + confidence) / 2, n - 2)
    y_pred = model.predict(x_with_const)
    se = np.sqrt(np.sum((y_values - y_pred) ** 2) / (n - 2))
    conf_interval = t_value * se * np.sqrt(1/n + (x_values - np.mean(x_values))**2 / np.sum((x_values - np.mean(x_values))**2))
    
    # Plot the data and the regression line with confidence intervals
    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, label='Data points')
    plt.plot(x_values, y_pred, color='red', label='Regression line')
    #plt.fill_between(x_values, y_pred - conf_interval, y_pred + conf_interval, color='red', alpha=0.2, label=f'{int(confidence*100)}% Confidence interval')
    plt.xlabel('Brightness')
    plt.ylabel('E (keV)')
    plt.legend()
    plt.title('Linear Regression')
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the plot
    plot_path = os.path.join(output_folder, 'linear_regression_plot.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved to {plot_path}")

# Example usage
x_values = [48, 14, 512, 440]  # Replace with your actual x values
y_values = [9.67, 8.39, 22.16, 17.48]  # Replace with your actual y values
output_folder = 'Code/brightness_regression/basler'  # Replace with the actual path to your output folder

linear_regression(x_values, y_values, output_folder, confidence=0.95)