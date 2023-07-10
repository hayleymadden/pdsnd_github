import time
import datetime
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_all = ('Chicago','New York City','Washington')
month_all = ("January", "February", "March", "April", "May", "June", "All")
dow_all = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All")

print("\nHello! Let\'s explore some US bikeshare data.\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Please select Chicago, New York City, or Washington to begin exploring bikeshare data: \n").title()
        if city not in city_all:
            print("\nHm, we don\'t have bikeshare data for that city. Please select Chicago, New York City, or Washington.\n")
            continue
        else: 
         break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("\nPlease select a month to explore the related bikeshare data: January, February, March, April, May, June, or ALL: \n").title()
        if month not in month_all:
            print("\nHm, we don\'t have bikeshare data for that month. Please select January, February, March, April, May, June, or ALL. \n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        dow = input("\nPlease select a day of the week to explore the related bikeshare data: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, ALL: \n").title()
        if dow not in dow_all:
            print("\nHm, we don't have bikeshare data for that day of the week. Please select Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, ALL. \n")
            continue
        else:
            message = "\nGreat, we\'ll look at bikeshare data in the city of {} during the month of {} and on the day of the week {}. \n"
            print(message.format(city, month, dow))
        break
            

    print('-'*40)

    return city, month, dow


def load_data(city, month, dow):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    

    """Handling for select_month that is not ALL"""
    if month != "All":
        df = df[df['month'] == month]
        
# filter by day of week to create the new dataframe

    if dow != "All":
        df = df[df['day_of_week'] == dow]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    
    common_month = df['month'].mode()[0]
    print("The most common month for bikeshare travel is", common_month)
    
    # Display the most common day of week
    
    common_day = df['day_of_week'].mode()[0]
    print("The most common day of the week for bikeshare travel is", common_day)

    # Display the most common start hour
    
    common_hour = df['hour'].mode()[0]
    print("The most common hour for bikeshare travel is", common_hour)
    
       
    print("\nThis operation took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common start station is ', common_start)
    
    # Display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station is ', common_end)

    # Display most frequent combination of start station and end station trip
    frequent_combo = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('The most frequently teaveled route is from ', frequent_combo)
    

    print("\nThis operation took %s seconds." % round((time.time() - start_time), 2))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The aggregate total travel time in days, hours:minutes:seconds format is ", str(datetime.timedelta(seconds=int(total_travel))))
    #total_travel = str(datetime.timedelta(seconds=60*60*24+1)) = df['Trip Duration'].sum()
    #seconds_passed = df['Trip Duration'].sum()
    #total_travel = str(datetime.timedelta(seconds=60*60*24+1))

    # Display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("The average Trip Duration in hours:minutes:secondsgit  format is ", (datetime.timedelta(seconds=int(avg_time))))

    print("\nThis operation took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        user_types = df['User Type'].value_counts()
        print('The count of each user type is: ', user_types)
    else:   
        print("Sorry, User Type data is not available for the selected city.")
    
    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts(dropna=True)
        print('The count of each gender is: ', gender_count)
    else:
        print("Sorry, Gender data is not available for the selected city.")

    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode(dropna=True)    
    
        message = "\nHere is some insight into user Birth Year data:\n The earliset Birth Year is {}\n The most recent Birth Year is {}\n The most common Birth Year is {}"
        print((message).format(int(earliest_birth_year), int(recent_birth_year),int(common_birth_year)))
    else:
        print("Sorry, Birth Year data is not available for the selected city.")

    print("\nThis operation took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)

def browse(df):
    """Gives the option to browse raw data for the selected city"""
    browse = input("\nWould you like to explore the underlying data for this city? Enter y or n\n").lower()
    index_start = 0
    index_stop = 4
    while True:
        if browse not in ("y", "n"):
            print("Hm, that input isn\'t recognized.  Please enter y or n.")
        if browse == "n":
            break
        if browse == "y":
            print(df.loc[index_start:index_stop])
            index_start += 5
            index_stop += 5
            browse = input("\nWould you like to load 5 more rows of underlying data? Enter y or n\n").lower()
        else:
            break


def main():
    while True:
        city, month, dow = get_filters()
        df = load_data(city, month, dow)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        browse(df)

        restart = input('\nWould you like to explore more bikeshare data? Enter Y or N.\n')
        if restart.upper() != 'Y':
            break


if __name__ == "__main__":
	main()
