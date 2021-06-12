import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './chicago.csv',
              'new york city': './new_york_city.csv',
              'washington': './washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    city_list = ['chicago','new york city','washington']
    while city not in city_list:
        city = input('Please select a city? (chicago/new york city/washington)   ').lower() 
        #add .lower() to make input not case sensitive
     
    # get user input for month (all, january, february, ... , june)
    # there are only 1-6 months in this data set 
    month = ''
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    while month not in month_list and month != 'all':
        month =input('Please select a month? (january/february/march/april/may/june) or write "all"    ').lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    day_list = ['monday','tuesday','wednesday','tuesday','friday','saturday','sunday']
    while day not in day_list and day != 'all':
        day = input('Please select a day? (monday/tuesday/wednesday/tuesday/friday/saturday/sunday), or write "all"    ').lower() 
    return city, month, day
   


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        city_data - Pandas DataFrame containing city data filtered by month and day
    """
    city_data = pd.read_csv(CITY_DATA[city])
    city_data['Start Time'] = pd.to_datetime(city_data['Start Time'])
    #extract month and day of week from Start Time to create new columns
    city_data['month'] = city_data['Start Time'].dt.month_name()
    #print(city_data.columns) used to check the data
    #print(city_data.info()) used to check the data
    city_data['day_of_week'] = city_data['Start Time'].dt.day_name()
   
    if month != 'all' :
        city_data = city_data[city_data['month'] == month.title()] 
        #city_data['month']=city_data[city_data['Start Time'].dt.month_name() == month.title()] alternative, we just wrote everything in one
    if day != 'all' :
        city_data = city_data[city_data['day_of_week'] == day.title()] 
        #here we could do the same as above all in one
    #print(city_data) check filtered db we work with in the stats
    return city_data


def time_stats(city_data):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    #print('Most common month %' %(city_data['month'].mode()[0]))
    print('\nMost Popular month: %s ' % (city_data['month'].mode()[0]))

    # display the most common day of week
    print('Most common day: %s' % (city_data['day_of_week'].mode()[0]))

    # display the most common start hour
    city_data['hour'] = city_data['Start Time'].dt.hour
    print('Most common hour: %s' % (city_data['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(city_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost common used start station: %s ' % (city_data['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nMost commonly used end station: %s ' % (city_data['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    
    city_data['combination'] = 'From ' + city_data['Start Station'].map(str) + ' to ' + city_data['End Station']
    
    print('\nMost frequent combination of start station and end station trip: %s ' % (city_data['combination'].mode()[0]))
  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(city_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time: %s ' % (city_data['Trip Duration'].sum()))
    
    # display mean travel time
    print('\nTotal mean time: %s ' % (city_data['Trip Duration'].mean()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city_data):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser Type information: %s ' % (city_data['User Type'].dropna(axis=0).value_counts()))
    
    try:
    # Display counts of gender
        print('\nGender information: %s ' % (city_data['Gender'].dropna(axis=0).value_counts()))
    except KeyError as e:
        print('This city does not have this data: %s ' % e )
    try:   
    # Display earliest, most recent, and most common year of birth
        print('\nEarlies birth year: %s ' % (city_data['Birth Year'].dropna(axis=0).min()))
        print('\nMost recent birth year: %s ' % (city_data['Birth Year'].dropna(axis=0).max()))
        print('\nMost common year of birth: %s ' % (city_data['Birth Year'].dropna(axis=0).mode()[0]))
    except KeyError as e:
        print('This city does not have this data: %s ' % e )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city_data):
    """Displays raw filtered data on request from the user."""
    data = 0
  
    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        if answer.lower() == 'yes':
            print(city_data[data : data+5])
            data += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        city_data = load_data(city, month, day)

        time_stats(city_data) #most popular times of travel (month, day, hour)
        station_stats(city_data) #most popular stations start, end, common trip start to end)
        trip_duration_stats(city_data) #total travel time, average travel time)
        user_stats(city_data) # counts of each user type, counts of each gender (NY,CH) earliest, most recent, most common year of birth (NY;CH))
        raw_data(city_data) # lists raw filtered data for the user 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        
        if restart.lower() != 'yes':
           break


if __name__ == "__main__": #python script should start with the main function in line 165
    main()
