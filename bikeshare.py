#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
print(os.getcwd())
import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[3]:


def get_filters():
    print("Hello! Let's explore some US bikeshare data!")

    cities = list(CITY_DATA.keys())
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday', 'all']

    while True:
        city = input("Enter city (Chicago, New York City, Washington): ").lower()
        if city in cities:
            break
        print("Invalid city. Please try again.")

    while True:
        month = input("Enter month (January–June) or 'all': ").lower()
        if month in months:
            break
        print("Invalid month. Please try again.")

    while True:
        day = input("Enter day (Monday–Sunday) or 'all': ").lower()
        if day in days:
            break
        print("Invalid day. Please try again.")

    print("-" * 40)
    return city, month, day


# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"Most Common Month: {months[common_month - 1]}")
    
    common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {common_day}")
    
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}:00")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    common_start = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {common_start}")
    
    common_end = df['End Station'].mode()[0]
    print(f"Most Common End Station: {common_end}")
    
    df['Trip'] = df['Start Station'] + " -> " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"Most Frequent Trip: {common_trip}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_duration = df['Trip Duration'].sum()
    days = total_duration // (24 * 3600)
    hours = (total_duration % (24 * 3600)) // 3600
    minutes = (total_duration % 3600) // 60
    seconds = total_duration % 60
    
    print(f"Total Travel Time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
    
    mean_duration = df['Trip Duration'].mean()
    mean_hours = mean_duration // 3600
    mean_minutes = (mean_duration % 3600) // 60
    mean_seconds = mean_duration % 60
    
    if mean_hours > 0:
        print(f"Average Travel Time: {int(mean_hours)} hours, {int(mean_minutes)} minutes, {int(mean_seconds)} seconds")
    else:
        print(f"Average Travel Time: {int(mean_minutes)} minutes, {int(mean_seconds)} seconds")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    print("User Types:")
    user_types = df['User Type'].value_counts()
    for user_type, count in user_types.items():
        print(f"  {user_type}: {count}")
    
    if 'Gender' in df.columns:
        print("\nGender Breakdown:")
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f"  {gender}: {count}")
    else:
        print("\nGender: Data not available for this city")
    
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        current_year = 2025
        oldest_age = current_year - earliest_year
        youngest_age = current_year - recent_year
        common_age = current_year - common_year
        
        print(f"\nBirth Year Stats:")
        print(f"  Oldest rider was born in {earliest_year} (age {oldest_age})")
        print(f"  Youngest rider was born in {recent_year} (age {youngest_age})")
        print(f"  Most common birth year is {common_year} (age {common_age})")
    else:
        print("\nBirth Year: Data not available for this city")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        row_index = 0
        while True:
            view_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").lower()
            if view_data == 'yes':
                print(df.iloc[row_index:row_index + 5])
                row_index += 5
                if row_index >= len(df):
                    print("\nNo more data to display.")
                    break
            else:
                break

        restart = input("\nWould you like to restart? Enter yes or no: ").lower()
        if restart != 'yes':
            print("\nThanks for exploring the bikeshare data! Have a great day! 🚴")
            break


if __name__ == '__main__':
    main()


# In[ ]:




