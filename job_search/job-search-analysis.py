#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 16:37:53 2025

@author: anujgawde
"""

import json
import psycopg2
import pandas as pd
from urllib.parse import urlparse

tmpPostgres = urlparse(database-connection-string)

DB_CONFIG = {
    "dbname": tmpPostgres.path.replace('/', ''),
    "user": tmpPostgres.username,
    "password": tmpPostgres.password,
    "host": tmpPostgres.hostname,
    "port": "5432",
}


# =============================================================================
# Fetch trending job searches based on keyword frequency.
# =============================================================================
def fetch_trending_jobs(location_filter=None, top_n=10):
    
    try:
        # Connecting to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Counting job searches grouped by keyword and location
        query = """
        SELECT keyword, location, COUNT(*) as search_count
        FROM job_searches
        WHERE (%s IS NULL OR location = %s)
        GROUP BY keyword, location
        ORDER BY search_count DESC
        LIMIT %s;
        """
        
        cursor.execute(query, (location_filter, location_filter, top_n))
        rows = cursor.fetchall()

        # Converting data into a DataFrame
        df = pd.DataFrame(rows, columns=['keyword', 'location', 'search_count'])

        # Converting DataFrame to a list of dictionaries (JSON serializable)
        trending_jobs = df.to_dict(orient='records')

        # Closing the connection
        cursor.close()
        conn.close()

        return json.dumps(trending_jobs)

    except Exception as e:
        return json.dumps({"error": str(e)})
    

# =============================================================================
# Analyze the correlation between experience level and preferred work mode
# =============================================================================
def fetch_experience_work_mode_trends():
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Query to count job searches grouped by experience level and work mode
        query = """
        SELECT experience_level, work_mode, COUNT(*) as search_count
        FROM job_searches
        WHERE experience_level IN ('Internship', 'Associate', 'Entry Level', 'Mid Senior Level', 'Director', 'Executive')
        AND work_mode IN ('On-Site', 'Remote', 'Hybrid')
        GROUP BY experience_level, work_mode
        ORDER BY experience_level, search_count DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=['experience_level', 'work_mode', 'search_count'])
        experience_work_mode_trends = df.to_dict(orient='records')

        cursor.close()
        conn.close()

        return json.dumps(experience_work_mode_trends)

    except Exception as e:
        return json.dumps({"error": str(e)})


# =============================================================================
# Analyze salary preferences based on experience level.
# =============================================================================
def fetch_experience_salary_trends():
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT experience_level, salary, COUNT(*) as count
        FROM job_searches
        WHERE experience_level IN ('Internship', 'Associate', 'Entry Level', 'Mid Senior Level', 'Director', 'Executive')
        AND salary IN ('$40,000+', '$60,000+', '$80,000+', '$100,000+', '$120,000+', '$140,000+', '$160,000+', '$180,000+', '$200,000+')
        GROUP BY experience_level, salary
        ORDER BY experience_level, count DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=['experience_level', 'salary', 'count'])
        experience_salary_trends = df.to_dict(orient='records')

        cursor.close()
        conn.close()

        return json.dumps(experience_salary_trends)

    except Exception as e:
        return json.dumps({"error": str(e)})


# =============================================================================
# Analyze salary preferences based on location.
# =============================================================================
def fetch_location_salary_trends():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT location, salary, COUNT(*) as count
        FROM job_searches
        WHERE salary IN ('$40,000+', '$60,000+', '$80,000+', '$100,000+', '$120,000+', '$140,000+', '$160,000+', '$180,000+', '$200,000+')
        GROUP BY location, salary
        ORDER BY location, count DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=['location', 'salary', 'count'])
        location_salary_trends = df.to_dict(orient='records')

        cursor.close()
        conn.close()

        return json.dumps(location_salary_trends)

    except Exception as e:
        return json.dumps({"error": str(e)})


# =============================================================================
# Find the most searched job title.
# =============================================================================
def fetch_most_searched_job_title():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT keyword, COUNT(*) as search_count
        FROM job_searches
        GROUP BY keyword
        ORDER BY search_count DESC
        LIMIT 1;
        """
        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return json.dumps({"most_searched_job_title": row[0], "search_count": row[1]})
        else:
            return json.dumps({"error": "No job searches found."})

    except Exception as e:
        return json.dumps({"error": str(e)})

