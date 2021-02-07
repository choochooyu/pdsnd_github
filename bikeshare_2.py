import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("\n- Would you like to see data for Chicago, New York City or Washington?\n").lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print("***Error-Please input a valid city name: Chicago, New York City or Washington***")

    # get the filter type by month, day or not at all
    while True:
        filter_type = input("\n- Would you like to filter the data by month, day or not at all?\n Please input month, day or none.\n").lower()
        if filter_type not in ('month', 'day','none'):
            print("***Error-Please choose from month, day or none.***")
        elif filter_type=='month':
            # get user input for month (all, january, february, ... , june)
            while True:
                month = input("\n- Select a month: January, February, March, April, May, June?\n").lower()
                day ='all'
                if month in ('january','february','march','april','may','june'):
                    break
                else:
                    print("**Error-Please input January, February, March, April, May, June")
            break
        elif filter_type == 'day':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:    
                day = input("\n- Select a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()  
                month='all'
                if day in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
                    break
                else:
                    print("**Error-Please input Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday")
            break
        elif filter_type == 'none':
            month = 'all'
            day = 'all'
            break
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
    #load data file into a dataframe
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
     # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    print("First 5 lines of data:")
    print(df.iloc[0:5])
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\nThe most common month is: ", df['month'].mode()[0])

    # display the most common day of week
    print("\nThe most common day of week is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    print("\nThe most common start hour is: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nThe most commonly used start station is: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("\nThe most commonly used end station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("\nThe most commonly used combination of start and end station is: ", (df['Start Station']+" and "+df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    def time_format(x):
        total_days =x//(60*60*24)
        hours=x%(60*60*24)//(60*60)
        minutes=x%(60*60*24)%(60*60)//60
        seconds=x%(60*60*24)%(60*60)%60
        return (total_days, hours, minutes, seconds)
    time_format(total_travel_time)
    print("\nThe total travel time is: {} days and {} hours and {} minutes and {} seconds.".format(*time_format(total_travel_time)))
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    time_format(total_travel_time)
    print("\nThe mean travel time is: {} days and {} hours and {} minutes and {} seconds.".format(*time_format(mean_time)))
    # display time taken to do the analysis
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users, such as the user types, gender, year of birth."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The counts of user types are:\n",user_types)

    # Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print("Gender Count for {} are:\n {}.".format(city,gender_count))

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_year = int(df['Birth Year'].min())
        print("\nEarliest year of birth for {} is {}.".format(city, earliest_year))
    
        most_recent_year = int(df['Birth Year'].max())
        print("\nMost recent year of birth for {} is {}.".format(city, most_recent_year))
    
        common_year = int(df['Birth Year'].mode()[0])
        print("\nMost common year of birth for {} is {}.".format(city, common_year))
    else:
        print("\nNo Gender/Birth Year data for Washington.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """ A function asking users if they would like to see 5 lines of raw data """
    count = 0

    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ').lower()
        # Check if response is yes, print the raw data and increment count by 5
        if answer == 'yes':
            print("\n5 lines of data:")
            print(df.iloc[count:count+5])
            count += 5
        # otherwise break
        if answer == 'no': 
            break
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
