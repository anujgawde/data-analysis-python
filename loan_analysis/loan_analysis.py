#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 14:05:52 2025

@author: anujgawde
"""

import pandas as pd;
import matplotlib.pyplot as plt;
import seaborn as sns;

# =============================================================================
# Classes        
# =============================================================================

        
class DataAnalysis:
    def __init__(self, df, column_name):
        self.df = df;
        self.column_name = column_name;
        
    def calculate_mean(self):
        return self.df[self.column_name].mean();
    
    def calculate_median(self):
        return self.df[self.column_name].median();
    


    
# =============================================================================
# Importing and Cleaning Data
# =============================================================================

loan_data = pd.read_excel('loandataset.xlsx');
customer_data = pd.read_csv('customer_data.csv', sep=';');

# Display the first few rows of our dataset
# print(loan_data.head())
# print(customer_data.head())

# Merging customer_data and loan_data on id
merged_data = pd.merge(loan_data, customer_data, left_on='customerid', right_on='id');

# Check for missing data
# print(merged_data.isnull().sum());

# Remove the rows with missing data
merged_data = merged_data.dropna();
# print(merged_data.isnull().sum());

# Check for duplicate data
# print(merged_data.duplicated().sum());

# Drop duplicate data
merged_data = merged_data.drop_duplicates();


# =============================================================================
# Methods
# =============================================================================


# Defining a function to create broader categories for loan purposes
def categorize_purpose(purpose):
    if purpose in ['credit_card', 'debt_consolidation']:
        return 'Financial'
    elif purpose in ['educational', 'small_business']:
        return 'Educational/Business'
    else:
        return 'Other'
    
    
    
# Analyze user's risk level:
    
# If the dti is greater than 20, delinq.2years is greater than 2, and revol.util>60 the particular loan is of high risk

# i. dti (Debt To Income): Amount of money the user pays for debt as compared to their income
# ii. delinq.2yrs: Data showing the number of times the user has defaulted payments etc. in the last 2 years
# iii. revol.util: Percentage of amount the user has taken from the loan granted to them

def analyze_risk(row):
    if row['dti'] > 20 and row['delinq.2yrs'] > 2 and row['revol.util'] > 60:
        return 'High Risk';
    else:
        return 'Low Risk';

# Categorizing on the basis of FICO Scores
def categorize_fico(fico_score):
    if(fico_score >= 800 and fico_score <= 850):
        return 'Excellent';
    elif fico_score >= 740 and fico_score < 800:
        return 'Very Good';
    elif fico_score >= 670 and fico_score < 740:
        return 'Good';
    elif fico_score >= 500 and fico_score < 670:
        return 'Fair';
    else:
        return 'Poor';
    
# Identify customers with more than average inquiries and derogatory records
def identify_high_inq_derog__cust(row):
    
    average_inq = merged_data['inq.last.6mths'].mean()
    average_derog = merged_data['pub.rec'].mean()
    
    if row['inq.last.6mths'] > average_inq and row['pub.rec'] > average_derog:
        return True;
    else:
        return False;
    
    

# =============================================================================
# Method Execution
# =============================================================================

# Categorizing loan purposes broadly using categorize_purpose:
merged_data['purpose_category'] = merged_data['purpose'].apply(categorize_purpose);


# Analyzing loan risk using analyze_risk:
merged_data['Risk'] = merged_data.apply(analyze_risk, axis=1)

  
# Categorizing on the basis of FICO Scores using categorize_fico
merged_data['Fico_Category'] = merged_data['fico'].apply(categorize_fico)


# Identify customers with more than average inquiries and derogatory records using identify_high_inq_derog__cust
merged_data['High_Inquiries_And_Public_Records'] = merged_data.apply(identify_high_inq_derog__cust, axis=1);


# Creating an instance of DataAnalysis Class:
fico_analysis = DataAnalysis(merged_data, 'fico')
mean_fico = fico_analysis.calculate_mean();
median_fico = fico_analysis.calculate_median();


# =============================================================================
# Data Visualization
# =============================================================================

sns.set_style('darkgrid')

# Bar Plot to show distribution of loans by purpose
plt.figure(figsize=(10,6))
sns.countplot(x = 'purpose', data = merged_data, palette='pastel')

plt.title('Loan Purpose Distribution');
plt.xlabel('Purpose of Loans');
plt.ylabel('Number of Loans')
plt.xticks(rotation=45)
plt.show()

# Scatterplot for 'dti' vs 'Income'
plt.figure(figsize=(10, 6))
sns.scatterplot(x = 'log.annual.inc', y='dti', data=merged_data)
plt.title('Debt to Income Ratio Vs. Annual Income')
plt.show()


# Distribution of FICO Scores
plt.figure(figsize=(10, 6))
sns.histplot(merged_data['fico'], bins=30, kde=True)
plt.title('Distribution of FICO Scores')
plt.show()


# Box plot to determine risk vs. interest rate
plt.figure(figsize=(10,6))
sns.boxplot(x='Risk', y='int.rate', data=merged_data);
plt.title('Interest Rate vs. Risk')
plt.show()








