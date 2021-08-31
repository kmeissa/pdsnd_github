# version notes: change longest trip approach, add more user and station stats
import time
import pandas as pd
import numpy as np


week_days = ["monday", "tuesday", "wednesday", "thursday",
             "friday", "saturday", "sunday", "all"]

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington).
    print("First, please tell me which city you are interested in - Chicago, New York City or Washington?")
    city = input("Please enter the city:  ").lower()
    while city not in ["chicago", "new york city", "washington"]:
        print("Oops I don't seem to understand your input")
        city = input("\nPlease enter Chicago, New York City or Washington:  ")
    print("")

    # get user input for month (all, january, february, ... , june)
    print("Do you wish to filter by month?")
    month = input("Please enter the month e.g. January, February, ..., June or all:  ").lower()
    while month not in ["january", "february", "march", "april", "may", "june", "all"]:
        try:
            type(int(month)) is int
            month = input("Please input the month by name, not number: ")
        except ValueError:
            print("I don't recognise your input.")
            month = input("Please enter the month e.g. January, February, ..., June or all:  ")
    print("")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Do you wish to filter by day?\nPlease enter the day of the week e.g. Monday, Tuesday... or all: ").lower()
    while day not in week_days:
        day = input("Oops I don't seem to understand your input!\nPlease enter the day of the week e.g. Monday, Tuesday... or all: ")
    # display user selected filters
    print("")
    print("Thanks! You are searching for data using the following filters:\nCity = {}\nMonth = {}\nDay = {}".format(city, month, day))
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
    # load data for user selected City
    df = pd.read_csv(CITY_DATA[city])

    # prepare df: convert start time and end time to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # prepare df: add month, day, hour, trip and travel time columns
    # to provide columns for user input filters and computing stats
    df["Month"] = df["Start Time"].dt.month
    df["Day"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour
    df["Journey"] = df["Start Station"] + "-" + df["End Station"]
    df["Travel Time"] = df["End Time"] - df["Start Time"]

    # month filter option, using index to create a filter for the dataframe
    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df["Month"] == month]

    # day filter option, using user input
    if day != 'all':
        df = df[df['Day'] == day.title()]

    # check if there is data before returning the datafraeme
    if df.empty:
        print("Sorry there is no data available for your filters")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df["Month"].mode()[0]
    print("Most popular month: ", popular_month)

    # display the most common day of week
    popular_day = df["Day"].mode()[0]
    print("Most popular day of the week: ", popular_day)

    # display the most common start hour
    popular_start_hour = df["Start Hour"].mode()[0]
    print("Most popular start hour: ", popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print("Most commonly used start station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("Most commonly used end station: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = df["Journey"].mode()[0].split("-")
    print("The most popular trip is from {} to {}".format(popular_trip[0], popular_trip[1]))

    # display the least frequently used start stations
    # least_used_start_station = ???
    # print("Most commonly used start station: ", popular_start_station)

    # display the total number of startions used in user filtered time frame
    df_count_unique = list(df.nunique())
    count_start = df_count_unique[4]
    count_end = df_count_unique[5]
    print("The total number of Start Stations used in this timeframe is: ", count_start)
    print("The total number of End Stations used in this timeframe is: ", count_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Travel Time"].sum()
    print("The total time travelling for all journeys: ", total_travel_time)

    # display mean travel time
    mean_travel_time = df["Travel Time"].mean()
    print("The average journey time: ", mean_travel_time)

    # display longest trip stats using max Travel Time
    df_longest_trip = df[df["Travel Time"] == df["Travel Time"].max()]
    print("The stats for the longest journey is as follows:")
    print(df_longest_trip[["Start Station", "End Station", "Travel Time"]])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The breakdown of user types is as follows:")
    print(df["User Type"].value_counts())

    # checks if the dataframe has Gender column
    column_name_list = df.columns.values.tolist()
    if "Gender" not in column_name_list:
        print("\nYour data does not contain information for Gender")
    # Display counts of gender
    else:
        print("\nThe gender split is as follows:")
        print(df["Gender"].value_counts())

    # checks if the dataframe has Birth Year column
    if "Birth Year" not in column_name_list:
        print("\nYour data does not contain information for Birth Year")
    # Display earliest, most recent, and most common year of birth
    else:
        print("\nHere are the stats for Birth Year:")
        print("The oldest user's birth year is: ", int(df["Birth Year"].min()))
        print("The youngest user's birth year is: ", int(df["Birth Year"].max()))
        print("The most common user birth year is: ", int(df["Birth Year"].mode()))
        print("The average user birth year is: ", int(df["Birth Year"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Displays 5 rows of raw data, per the users input filters.
    Iterates through 5 additional lines until user inputs 'no' to prompt
    or there are no futher rows in the dataframe.
    Inputs:
        No to exit
        Enter (or any other input) to continue
    Returns:
        5 lines of df (Pandas DataFrame) from original source data
    """

    print("\nWould you like to view some raw data?")
    lines_of_raw_data = input("\nHit Enter for 5 new lines, or enter No to exit: ").lower()
    x = 0
    while lines_of_raw_data != 'no':
        # increment the start and end index position by 5
        x = x + 5
        y = x + 5
        print(df.iloc[x:y])
        lines_of_raw_data = input("\nHit Enter for 5 new lines, or enter No to exit: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        user_stats(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
