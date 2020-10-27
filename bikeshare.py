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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter a city, choosing from \"Chicago\", \"New York City\", or \"Washington\": ").lower()
    while city not in CITY_DATA.keys():
        print("You did not correctly select one of the 3 cities. Please enter the city again.")
        city = input("Please enter a city for which you would like more information, choosing from \"Chicago\", \"New York City\", or \"Washington\": ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter the month that you are interested in (from range January - June). Type \"all\" if you do not want to filter by month : ").lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june','all']:
        print("You did not correctly select a month from the range January - June or selected \"all\". Please enter the month(s) you are interested in again.")
        month = input("Please enter the month that you are interested in (from range January - June). Type \"all\" if you do not want to filter by month : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the weekday (Monday - Sunday) in which you are interested. Type \"all\" if you do not want to filter by weekday: ").lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']:
        print("You did not correctly select a weekday. Please enter the weekday(s) you are interested in again.")
        day = input("Please enter the weekday (Monday - Sunday) in which you are interested. Type \"all\" if you do not want to filter by weekday: ").lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
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

    return df

# function that attests whether all values in a dataframe column are identical
def is_unique(s):
    a = s.to_numpy()
    return (a[0] == a).all()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month
    # map month number to month name (string)
    months_dict = {1: 'January', 2: 'February', 3:'March', 4: 'April', 5: 'May', 6: 'June'}
    popular_month_no = df['month'].mode()[0]
    popular_month = months_dict[popular_month_no]
    # only show popular month if user select "all" - else display month chosen by user
    if is_unique(df['month']) == False:
        print('\nThe most popular month to travel was {}.'.format(popular_month))
    else:
        print('\nIn the month of {}:'.format(popular_month))

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    # only show popular month if user select "all" - else display month chosen by user
    if is_unique(df['day_of_week']) == False:
        print('\nThe most popular day of week to travel was {}.'.format(popular_day_of_week))
    else:
        print('\nOn {}s: \n'.format(popular_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most popular start hour was {}.\n'.format(popular_hour))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('\nThe most popular start station was {}.'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\nThe most popular end station was {}.'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ' and ' + df['End Station']
    most_common_start_end_station = df['Start and End Station'].mode()[0]
    print('\nThe most popular start station and end station combination was {} respectively.\n'.format(most_common_start_end_station))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    total_travel_time_sec = df['Trip Duration'].sum()
    total_travel_time_min = int(total_travel_time_sec / 60)
    print('\nThe total travel time of all trips was {} minutes.'.format(total_travel_time_min))

    # display mean travel time
    mean_travel_time_sec = df['Trip Duration'].mean()
    mean_travel_time_min = int(mean_travel_time_sec / 60)
    print('\nThe mean travel time per ride was {} minutes.\n'.format(mean_travel_time_min))

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe counts per user type were as follows:\n')
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('\nThe counts per gender were as follows:\n')
        print(gender)
    else:
        print('\nThere is no gender information available for users in the city you selected.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nThe oldest user was born in {}, the youngest in {}, and the most common user birth year was {}.\n'.format(earliest_birth_year,latest_birth_year,most_common_birth_year))
    else:
        print('\nThere is no birth year information available for users in the city you selected.\n')

    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to continue?: ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        print("-"*20)
        station_stats(df)
        print("-"*20)
        trip_duration_stats(df)
        print("-"*20)
        user_stats(df)
        print("-"*20)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
