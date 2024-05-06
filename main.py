import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_path = './XAU_USD_1975_2024.csv'
gold_data = pd.read_csv(data_path)


# Convert 'Price' and 'Open' from string to float and remove commas
gold_data['Price'] = gold_data['Price'].str.replace(',', '').astype(float)
gold_data['Open'] = gold_data['Open'].str.replace(',', '').astype(float)

# Determine the trend of each month
def determine_trend(row):
    if row['Price'] > row['Open']:
        return 'Bullish'
    elif row['Price'] < row['Open']:
        return 'Bearish'
    else:
        return 'Range'

gold_data['Trend'] = gold_data.apply(determine_trend, axis=1)

# Convert 'Date' to datetime and extract month and year
gold_data['Date'] = pd.to_datetime(gold_data['Date'], format='%m/%d/%Y')
gold_data['Month'] = gold_data['Date'].dt.month
gold_data['Year'] = gold_data['Date'].dt.year

# Group by month and count the occurrences of each trend
monthly_trend_summary = gold_data.groupby('Month')['Trend'].value_counts().unstack(fill_value=0)
# print(monthly_trend_summary)
# Handle no 'Range' data
if 'Range' not in monthly_trend_summary:
    monthly_trend_summary['Range'] = 0

# Calculate the total and percentages
monthly_trend_summary['Total'] = monthly_trend_summary.sum(axis=1)
for trend in ['Bullish', 'Bearish', 'Range']:
    monthly_trend_summary[f'Percent {trend}'] = (monthly_trend_summary[trend] / monthly_trend_summary['Total']) * 100

# Reset index to include 'Month' as a column
monthly_trend_summary.reset_index(inplace=True)

# Visualization with Matplotlib
fig, ax = plt.subplots(figsize=(14, 10))
positions = list(range(len(monthly_trend_summary['Month'])))
width = 0.25

# Plotting the data with updated colors
plt.bar([p - width for p in positions], monthly_trend_summary['Percent Bullish'], width, alpha=0.5, color='green', label='Bullish')
plt.bar(positions, monthly_trend_summary['Percent Bearish'], width, alpha=0.5, color='red', label='Bearish')
plt.bar([p + width for p in positions], monthly_trend_summary['Percent Range'], width, alpha=0.5, color='blue', label='Range')

ax.set_ylabel('Percentage')
ax.set_title('Monthly Gold Price Trends (1975-2024)')
ax.set_xticks(positions)
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Adding the table below the chart
cell_text = []
for row in range(len(monthly_trend_summary)):
    # print(row)
    cell_text.append([
        monthly_trend_summary.loc[row, 'Bullish'],
        monthly_trend_summary.loc[row, 'Bearish'],
        monthly_trend_summary.loc[row, 'Range'],
        f"{monthly_trend_summary.loc[row, 'Percent Bullish']:.2f}%",
        f"{monthly_trend_summary.loc[row, 'Percent Bearish']:.2f}%",
        f"{monthly_trend_summary.loc[row, 'Percent Range']:.2f}%"
    ])
# print(monthly_trend_summary)
table = plt.table(cellText=cell_text,
                  rowLabels=monthly_trend_summary['Month'].apply(lambda x: pd.to_datetime(x, format='%m').strftime('%b')),
                  colLabels=['Bullish', 'Bearish', 'Range', '% Bullish', '% Bearish', '% Range'],
                  cellLoc = 'center', rowLoc = 'center',
                  loc='bottom', bbox=[0.0, -0.7, 1.0, 0.6])

# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.4)

ax.legend()
plt.show()
plt.savefig('Figure_2.png')