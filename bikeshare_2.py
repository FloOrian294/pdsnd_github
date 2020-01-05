import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
ACRONYM_CITY_DATA = {   'chi': 'chicago',
                        'chic': 'chicago',
                        'ny': 'new york city',
                        'nyc': 'new york city',
                        'new york': 'new york city',
                        'wash': 'washington',
                        'd.c.': 'washington',
                        'dc': 'washington'}

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
ACRONYM_MONTH_DATA = {  'al': 'all',
                        '1': 'january',
                        '01': 'january',
                        'jan': 'january',
                        '2': 'february',
                        '02': 'february',
                        'feb': 'february',
                        '3': 'march',
                        '03': 'march',
                        'mar': 'march',
                        '4': 'april',
                        '04': 'april',
                        'apr': 'april',
                        '5': 'may',
                        '05': 'may',
                        'mai': 'may',
                        '6': 'june',
                        '06':'june',
                        'jun':'june'}

DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
ACRONYM_DAY_DATA = {    'mon': 'monday',
                        'tue': 'tuesday',
                        'wed': 'wednesday',
                        'thu': 'thursday',
                        'fri': 'friday',
                        'sat': 'saturday',
                        'sun': 'sunday'}

"Please choose one of the three cities data  available for: Chicago, New York City or Washington!"
# function to check if input was intended to match with required input
# check if str_input  a key of dict_input
# if TRUE: return value of dict corresponding to key and set repeat_input to FALSE
# if FALSE: return empty string ans set repeat_input to TRUE
def check_acronym_data(str_input,dict_input,text):
    str_output = ''
    repeat_input = True
    if dict_input.get(str_input) == None:
        print(text)
    else:
        choice = input("Did you choose {}\nPlease confirm with y or get a new chance to choose the city by typing any input!".format(dict_input.get(str_input).capitalize()))
        if choice == 'y':
            str_output = dict_input.get(str_input)
            # stop input for cities
            repeat_input = False

    return repeat_input, str_output

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\nDatasets of the first half of 2017 are availble and analyzing it by day, month or over the whole period  possible.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # variable to control input flow
    input_loop = True
    city = ''
    while input_loop:
        city = input("You have the choice to analyze data from three different cities. Chicago, New York City or Washington.\nPlease let me know from which city do you want to explore US bikeshare data?").lower().strip()
        if CITY_DATA.get(city) == None:
            # deal with input that  not expected
            input_loop, city = check_acronym_data(city,ACRONYM_CITY_DATA,"Please choose one of the three cities data  available for: Chicago, New York City or Washington!")
            # if city acronym was matched to city get filename of CITY_DATA
            if not input_loop:
                city_filename = CITY_DATA.get(city)
        else:
            city_filename = CITY_DATA.get(city)
            # stop input for cities
            input_loop = False

    # get user input for month (all, january, february, ... , june)
    # reste variable to control input flow
    input_loop = True
    month = ''
    while input_loop:
        month = input("Please choose the month you are interested in or type all if you are not intested in a specific month?)").lower().strip()
        if not (month in MONTH_DATA):
            input_loop, month = check_acronym_data(month,ACRONYM_MONTH_DATA,"Please type in the full name of the month you are interested in or type all?")
        else:
            # stop input for months
            input_loop = False#


    # get user input for day of week (all, monday, tuesday, ... sunday)
    input_loop = True
    day = ''
    while input_loop:
        day = input("Please choose the day you are interested in or type all if you are not intested in a specific day?)").lower().strip()
        if not (day in DAY_DATA):
            input_loop, day = check_acronym_data(day,ACRONYM_DAY_DATA,"Please type in the full name of the day you are interested in or type all?")
        else:
            # stop input for months
            input_loop = False

    print('-'*40)
    #Recapitalize New York City
    if city == 'new york city':
        single_words = city.split()
        city = ''
        for val in single_words:
            city += val.capitalize() + ' '
        city = city.strip()
    else:
        city = city.capitalize()

    if (month == 'all' and day == 'all'):
        print('You are interested in datas of {} of the first half of the year 2017!'.format(city))
    elif month == 'all':
        print('You are interested in datas of {} on {}s of the first half of the year 2017!'.format(city, day))
    elif day == 'all':
        print('You are interested in datas of {} of {} of the year 2017!'.format(city, month.capitalize()))
    else:
        print('You are interested in datas of {} of {} on {}s of the year 2017!'.format(city, month.capitalize(), day))
    return city_filename,city, month, day


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
    #read data
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.dayofweek
    df['Start hour'] = df['Start Time'].dt.hour

    df_filter = df
    #debug
    print(df.head())
    #filter by month
    if month != 'all':
        index_month = MONTH_DATA.index(month)
        df_filter = df[df['Month'] == index_month]
    #debug
    #print(df.head())
    #filter by day
    if day != 'all':
        index_day = DAY_DATA.index(day)
        df_filter = df[df['Weekday'] == index_day]

    #debug
    #print(df.head())
    return df, df_filter


def time_stats(df, city):
    """displays stattics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times in {} of Travel for the first half of 2017 ...\n'.format(city))
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('Most common month: {}'.format(MONTH_DATA[popular_month].capitalize()))

    # display the most common day of week
    popular_day = df['Weekday'].mode()[0]
    print('Most common weekday: {}'.format(DAY_DATA[popular_day].capitalize()))


    # display the most common start hour
    popular_hour = df['Start hour'].mode()[0]
    print('Most comm start hour: {}'.format(popular_hour))

    print("\nTh took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, weekday):
    """displays stattics on the most popular stations and trip"""
    if (month == 'all' and weekday == 'all'):
        print('\nCalculating The Most Popular Stations and Trip in {} in first half of 2017...\n'.format(city))
    elif month == 'all':
        print('\nCalculating The Most Popular Stations and Trip in {} in first half of 2017 on {}s...\n'.format(city, weekday.capitalize()))
    elif weekday == 'all':
        print('\nCalculating The Most Popular Stations and Trip in {} in {} 2017...\n'.format(city, month.capitalize()))
    else:
        print('\nCalculating The Most Popular Stations and Trip in {} in {} 2017 on {}s...\n'.format(city, month.capitalize(), weekday.capitalize()))

    start_time = time.time()

    # display most commonly used start station
    if 'Start Station' in df.columns:
        popular_start_station = df['Start Station'].mode()[0]
        print('Most commonly used start station  {}'.format(popular_start_station))
    else:
        print('Unfortunately the dataset is missing data wrt Start Station.')
    # display most commonly used end station
    if 'End Station' in df.columns:
        popular_end_station = df['End Station'].mode()[0]
        print('Most commonly used end station  {}'.format(popular_end_station))
    else:
        print('Unfortunately the dataset is missing data wrt End Station.')

    if ('Start Station' in df.columns and 'End Station' in df.columns):
    # display most frequent combination of start station and end station trip
        popular_combination_start_end_station = df[['Start Station', 'End Station']].mode()
        print('Most frequent combination of start and end station :\nStart Station: {}\nEnd Station: {}'.format(popular_combination_start_end_station['Start Station'][0], popular_combination_start_end_station['End Station'][0]))
    else:
        print('Unfortunately the dataset is missing data wrt Start or End Station.')


    print("\nTh took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, weekday):
    """displays stattics on the total and average trip duration."""
    if (month == 'all' and weekday == 'all'):
        print('\nCalculating Trip Duration in {} in first half of 2017...\n'.format(city))
    elif month == 'all':
        print('\nCalculating Trip Duration in {} in first half of 2017 on {}s...\n'.format(city, weekday.capitalize()))
    elif weekday == 'all':
        print('\nCalculating Trip Duration in {} in {} 2017...\n'.format(city, month.capitalize()))
    else:
        print('\nCalculating Trip Duration in {} in {} 2017 on {}s...\n'.format(city, month.capitalize(), weekday.capitalize()))

    start_time = time.time()

    if 'Trip Duration' in df.columns:
        # display total travel time
        total_travel_time = str(df['Trip Duration'].sum())
        print('The total travel time  {} sec.'.format(total_travel_time))

        # display mean travel time
        avg_travel_time = str(df['Trip Duration'].mean())
        print('The total average time  {} sec.'.format(avg_travel_time))
    else:
        print('Unfortunately the dataset is missing data wrt Trip Duration.')

    print("\nTh took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, weekday):
    """displays statistics on bikeshare users."""
    if (month == 'all' and weekday == 'all'):
        print('\nCalculating User Stats in {} in first half of 2017...\n'.format(city))
    elif month == 'all':
        print('\nCalculating User Stats in {} in first half of 2017 on {}s...\n'.format(city, weekday.capitalize()))
    elif weekday == 'all':
        print('\nCalculating User Stats in {} in {} 2017...\n'.format(city, month.capitalize()))
    else:
        print('\nCalculating User Stats in {} in {} 2017 on {}s...\n'.format(city, month.capitalize(), weekday.capitalize()))

    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print('Distribution of User Types:')
        for key in user_types.keys():
            print(' {} {}'.format(key, user_types.get(key)))
    else:
        print('Unfortunately the dataset is missing data wrt User Type.')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Distribution of Gender:')
        for key in gender.keys():
            print(' {} {}'.format(key, gender.get(key)))
    else:
        print('Unfortunately the dataset is missing data wrt Gender.')
    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = str(int(df['Birth Year'].min()))
        print('\nThe oldest driver  born in {}'.format(earliest_year_of_birth))
        most_recent_year_of_birth = str(int(df['Birth Year'].max()))
        print('The youngest driver  born in {}'.format(most_recent_year_of_birth))
        popular_year_of_birth = str(int(df['Birth Year'].mode()[0]))
        print('Most drivers are born in {}'.format(popular_year_of_birth))
    else:
        print('Unfortunately the dataset is missing data wrt Birth Year.')

    print("\nTh took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city_filename, city, month, day = get_filters()
        df, df_filter = load_data(city_filename, month, day)

        time_stats(df,city)
        station_stats(df_filter, city, month, day)
        trip_duration_stats(df_filter, city, month, day)
        user_stats(df_filter, city, month, day)

        #Print individual data
        print_individual_data = input('For getting individual data sets enter y!')
        dataset_low = 0
        dataset_high = 10
        dataset_max = df.shape[0]
        while print_individual_data == 'y':
            print(df[dataset_low:dataset_high])
            dataset_low += 10
            dataset_high += 10
            if dataset_high > dataset_max:
                print('No more individual data available.')
                print_individual_data = 'n'
            else:
                print_individual_data = input('For more individual data enter y!')

        restart = input('\nWould you like to restart? Confirn with y or quit with any input.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
