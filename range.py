import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_path = './XAU_USD_2000_2024.csv'
gold_data = pd.read_csv(data_path)

# Convert 'Price', 'Open', 'High', 'Low' from string to float and remove commas
gold_data['Price'] = gold_data['Price'].str.replace(',', '').astype(float)
gold_data['Open'] = gold_data['Open'].str.replace(',', '').astype(float)
gold_data['High'] = gold_data['High'].str.replace(',', '').astype(float)
gold_data['Low'] = gold_data['Low'].str.replace(',', '').astype(float)

# Convert 'Date' to datetime and extract month and year
gold_data['Date'] = pd.to_datetime(gold_data['Date'], format='%m/%d/%Y')
gold_data['Month'] = gold_data['Date'].dt.month
gold_data['Year'] = gold_data['Date'].dt.year

# Group by month and calculate the monthly high and low
monthly_high_low = gold_data.groupby(['Year', 'Month']).agg({'High': 'max', 'Low': 'min'}).reset_index()

# Calculate the range as high - low, then convert to pips by multiplying by 10
monthly_high_low['Range'] = (monthly_high_low['High'] - monthly_high_low['Low']) * 10

# Calculate the average range for each month across all years
average_monthly_range = monthly_high_low.groupby('Month')['Range'].mean()

# Convert this to a DataFrame for easier plotting
monthly_range_summary = average_monthly_range.reset_index()
monthly_range_summary.columns = ['Month', 'Average Range in Pips']

# Replace numeric months with month names and format the 'Average Range in Pips' to two decimal places
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_range_summary['Month'] = monthly_range_summary['Month'].apply(lambda x: month_names[x-1])
monthly_range_summary['Average Range in Pips'] = monthly_range_summary['Average Range in Pips'].apply(lambda x: f"{x:.2f}")

# Visualization with Matplotlib
fig, ax = plt.subplots(figsize=(14, 10))
positions = list(range(len(monthly_range_summary['Month'])))

# Plotting the average range in pips
bars = plt.bar(positions, monthly_range_summary['Average Range in Pips'].astype(float), alpha=0.5, color='blue', label='Average Monthly Range in Pips')

ax.set_ylabel('Average Range in Pips')
ax.set_title('Average Monthly Range in Pips for Gold Prices (2000-2024)')
ax.set_xticks(positions)
ax.set_xticklabels(month_names)

# Adding a table
table_data = monthly_range_summary.values
table = plt.table(cellText=table_data,
                  colLabels=monthly_range_summary.columns,
                  colLoc='center',
                  cellLoc='center',
                  loc='bottom',
                  bbox=[0, -0.5, 1, 0.4])  # Adjust bbox to fit the table below the axes

plt.subplots_adjust(left=0.2, bottom=0.2)  # Make space for the table

ax.legend()
plt.show()
plt.savefig('Average_Monthly_Range_in_Pips_Gold_Prices.png', bbox_inches='tight')  # Ensure the whole figure, including table, is saved
