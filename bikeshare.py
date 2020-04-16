import time
import datetime
import pandas as pd
import numpy as np
from calendar import month_name

# input files are required in local directory
# special note: washington does not have user stats

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ""
    month = ""
    day = ""
    
    # Done: get user input for city (chicago, new york city, washington). 
    while True:
        city = input('Enter Requested City (or Stop): ')
        city = city.lower().strip()
        if (city in CITY_DATA) or (city == 'stop'):
            break
        else: 
            print('Valid City list is chicago, new york city, washington')

           
    # Done: get user input for month (all, january, february, ... , june)
    if city != 'stop':
        
        while True:
            month = input('Enter Requested Month (or All or Stop): ')
            month = month.title().strip()
            if (month == 'All') or (month in month_name) or (month == 'Stop'):
                break
            else: 
                print('Month must be entered as All or a valid Month (January thru December)')
        
    # Done: get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    if city != 'stop' and month != 'Stop':
        
        while True:
            day = input('Enter Requested Day (or All or Stop): ')
            day = day.title().strip()
            if (day == 'All') or (day in weekdays) or (day == 'Stop'):
                break
            else: 
                print('Day must be entered as All or a valid Weekday (Sunday thru Saturday)')

    
    
    print('-'*40)
    return city, month, day


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
    
    week_days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    month_names= ['January', 'February', 'March', 'April', 'May', 'June','July',
                  'August', 'September', 'October', 'November', 'December']
    
   # get the filename based on city input
    filename = CITY_DATA.get(city)
    
    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert Start Time to datetime and create columns for the month and day
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    df['month'] = df['Start Time'].apply(lambda time: time.month)    
    df['day'] = df['Start Time'].apply(lambda time: time.dayofweek)

    # filter down to the selected month 
    if month != 'All':
        month_filter = month_names.index(month)+1 
        df = df[df['month']==month_filter]

    # filter down to the selected day
    if day != 'All':
        day_filter = week_days.index(day)+1 
        df = df[df['day']==day_filter]
   

    # I need to make sure there is somethimg in the dataframe 
    if df.empty:
        print('no results, please alter search and try again...')
          
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    week_days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    month_names= ['January', 'February', 'March', 'April', 'May', 'June','July',
                  'August', 'September', 'October', 'November', 'December']
                      
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Done: display the most common month
    # use the mode to get most common
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', month_names[most_common_month-1])

    # Done: display the most common day of week
    # use the mode to get most common
    most_common_day = df['day'].mode()[0]
    print('Most Common Day of Week:', week_days[most_common_day-1])


    # Done: display the most common start hour
    # get the hour 
    df['hour'] = df['Start Time'].dt.hour
    # use the mode to get most common
    most_common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    

    ### testing here print(df.groupby(['Start Station']).count())
    
    # Done: display most commonly used start station
    print('Most Common Start Station:', df['Start Station'].mode()[0])

    # Done: display most commonly used end station
    print('Most Common End Station:', df['End Station'].mode()[0])


    # Done: display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most Common Start Station / End Station:', df['start_end'].mode()[0])
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Done: display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # Done: display mean travel time
    print('Mean travel time:',np.mean(df['Trip Duration']))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
                      
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Done: Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print("Counts by User Type")
    print(user_types)

    # Done: Display counts of gender
    gender = df['Gender'].value_counts()
    print("Counts by Gender")
    print(gender)

    # Done: Display earliest, most recent, and most common year of birth
    print('Most recent year of birth:',df['Birth Year'].max())
    print('Earliest year of birth:',df['Birth Year'].min())
    print('Most Common year of birth:', df['Birth Year'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        
        if city == 'stop' or month == 'Stop' or day == 'Stop':
            break
                    
        df = load_data(city, month, day)

        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            if city == 'washington':
                print("No user stats for selected city")
            else:
                user_stats(df)
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
