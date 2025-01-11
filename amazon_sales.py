#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 15:14:41 2025

@author: anujgawde

Questions to be answered:
    
    - How many sales have they made with amounts more than 1000
    - How many sales have they made that belong to the Cateogry 'Tops' and have a quantity of 3
    - The total sales by category
    - Average amount by category and status
    - Total Sales by fulfilment and shipment type

"""

import pandas as pd;


sales_data = pd.read_excel('sales_data.xlsx');

# =============================================================================
# Exploring the data
# =============================================================================


# get a summary of sales data
sales_data.info(); # can also check for datatypes here

# Brief description of the data
sales_data.describe();


# looking at columns
print(sales_data.columns)


# having a look at the first few rows of data
print(sales_data.head());

# check the data types of the columns
print(sales_data.dtypes);

# =============================================================================
# Cleaning the data
# =============================================================================

# check for missing values in our sales data
# print(sales_data.isnull().sum()) # In order to access the number of null rows in the column
print(sales_data.isnull())

# dropping data with any null data
sales_data_dropped = sales_data.dropna();

# dropping data with null amount column
sales_data_cleaned = sales_data.dropna(subset= ['Amount'])

print(sales_data_cleaned.isnull().sum())


# =============================================================================
# Slicing and Filtering Data
# =============================================================================


# selecting a subset of our data based on the category column
category_data = sales_data[sales_data['Category'] == 'Top']
print(category_data)

# Select a subset of our data where the Amoun > 1000
high_amount_data = sales_data[sales_data['Amount'] > 1000]
print(high_amount_data)

# Selecting a subset of data based on multiple conditions
filtered_data = sales_data[(sales_data['Category'] == 'Top') & (sales_data['Qty'] == 3)]


# =============================================================================
# Aggregating Data
# =============================================================================

# Calculating the total sales by category

category_totals = sales_data.groupby('Category')['Amount'].sum()
category_totals = sales_data.groupby('Category', as_index=False)['Amount'].sum()
category_totals = category_totals.sort_values('Amount', ascending=False)


# Calculate the average amount by category and fulfilment
fulfilment_averages = sales_data.groupby(['Category', 'Fulfilment'], as_index=False)['Amount'].mean()
fulfilment_averages = fulfilment_averages.sort_values('Amount', ascending=False)


# Calculate the average by category and status
status_averages = sales_data.groupby(['Category', 'Status'], as_index=False)['Amount'].mean()
status_averages = status_averages.sort_values('Amount', ascending=False)


# Calculate total sales by shipment and fulfilmemt
total_sales_ship_fulfil = sales_data.groupby(['Courier Status', 'Fulfilment'], as_index=False)['Amount'].sum()
total_sales_ship_fulfil = total_sales_ship_fulfil.sort_values('Amount', ascending=False)

total_sales_ship_fulfil.rename(columns={'Courier Status': 'Shipment'}, inplace=True)


# =============================================================================
# Exporting the data
# =============================================================================

status_averages.to_excel('average_sales_by_category_and_status.xlsx', index=False)
total_sales_ship_fulfil.to_excel('total_sales_by_shipment_and_fulfilment.xlsx')



 
 




