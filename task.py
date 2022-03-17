import csv
import pytest


# Q1:- how many total number of days does the flights table cover?

# As there are many duplicate days. because there are so many fligts on same day.
# That's why here my approach is, using built-in 'set' data structure we can store
# unique days available in the file then return the length of the set to return total number of days.


def total_number_of_days(flights_file):
    """
    returns the total number of days in given csv file.
    """
    unique_days = set()
    with open(flights_file) as flights:
        csv_reader = csv.DictReader(flights)
        for line in csv_reader:
            date = (line["year"], line["month"], line["day"])
            unique_days.add(date)
    return len(unique_days)


# Q2:- how many departure cities (not airports) does the flights database cover?

# Here my approach is store all the unique departure airports in the list.
# Then loop through those and and airports database at the same time to get the cities.


def departure_cities(flights_file, airports_file):
    """
    returns the cities that the flights database cover.
    """
    departure_airports = []
    cities = set()
    with open(flights_file) as flights:
        flights_reader = csv.DictReader(flights)
        for line in flights_reader:
            if line["origin"] not in departure_airports:
                departure_airports.append(line["origin"])

    with open(airports_file) as airports:
        airports_reader = csv.DictReader(airports)
        for line in airports_reader:
            for airport in departure_airports:
                if line["IATA_CODE"] == airport:
                    cities.add(line["CITY"])
    return cities


# Q3:- what is the relationship between flights and planes tables?

# Here I'm getting the expected output by using List Comprehensions.


def relationship(flights_file, planes_file):
    """
    returns the relationship between two databases.
    """
    with open(flights_file) as flights:
        flights_reader = csv.reader(flights)
        flights_coloums = next(flights_reader)
        with open(planes_file) as planes:
            planes_reader = csv.reader(planes)
            planes_coloums = next(planes_reader)
            relationship = [
                relation for relation in flights_coloums if relation in planes_coloums
            ]
    if not relationship:
        return None
    return relationship


# Q4:- which airplane manufacturer incurred the most delays in the analysis period?

# Firstly we have to findout how much total delay each plane has done. delay couldn't be
# negative right, means it is arrived early or departed early which is not the delay and not a bad thing as well.
# So here I'm counting both delays.

# Again, to store all the plane models with its total delay, I'm using dictionaries.


def manufacturer_with_most_delays(flights_file, planes_file):
    """
    returns the manufacturer of the plane, which has done most amount of delay.
    """
    tailnums_with_delay_count = dict()
    result = ""
    with open(flights_file) as flights:
        flights_reader = csv.DictReader(flights)
        for line in flights_reader:
            tailnum = line["tailnum"]
            # Parsing the delays to get the proper values. as there are other values as well like 'NA'
            arr_delay = "".join(x for x in line["arr_delay"] if x.isdigit())
            dep_delay = "".join(x for x in line["dep_delay"] if x.isdigit())
            # simply checking is plane model already in the dictionary.
            if line["tailnum"] not in tailnums_with_delay_count:
                if arr_delay != "" and dep_delay != "":
                    if int(dep_delay) > 0 and int(arr_delay) > 0:
                        tailnums_with_delay_count[tailnum] = int(arr_delay) + int(
                            dep_delay
                        )
                elif dep_delay != "":
                    if int(dep_delay) > 0:
                        tailnums_with_delay_count[tailnum] = int(dep_delay)
                elif arr_delay != "":
                    if int(arr_delay) > 0:
                        tailnums_with_delay_count[tailnum] = int(arr_delay)
                else:
                    line["tailnum"] = 0
            # If it is already in the dictionary. We are adding the delay count to existing one.
            else:
                if arr_delay != "" and dep_delay != "":
                    if int(dep_delay) > 0 and int(arr_delay) > 0:
                        tailnums_with_delay_count[tailnum] += int(arr_delay) + int(
                            dep_delay
                        )
                elif dep_delay != "":
                    if int(dep_delay) > 0:
                        tailnums_with_delay_count[tailnum] += int(dep_delay)
                elif arr_delay != "":
                    if int(arr_delay) > 0:
                        tailnums_with_delay_count[tailnum] += int(arr_delay)
    # Sorting the dictionary to get the plane model which has done most delay.
    # but here comes the challenging part again. There is no entry in the planes
    # database with has done most delay.
    sorted_delayed_tailnums = sorted(
        tailnums_with_delay_count.items(), key=lambda item: item[1]
    )
    # That's why iterating through the the sorted dictionary from behind.
    # And checking if the plane model in present in the planes database or not
    # to get the manufacturer of the plane.
    i = 1
    while i < len(sorted_delayed_tailnums):
        with open(planes_file) as planes:
            planes_reader = csv.DictReader(planes)
            for line in planes_reader:
                if line["tailnum"] == sorted_delayed_tailnums[-i][0]:
                    result = line["manufacturer"]
                    i = len(sorted_delayed_tailnums)
        i += 1
    return result


# Q5:- which are the two most connected cities?

# Here my approach is using built-in dictionaries. By storing the connected airports as a tuple in the dictionary with its count,
# After sorting the dictionary we'll get the most connected airports. Which would be last key value pair.
# Then we can simply lookup the values in airports database.


def two_most_connected_cities(flights_file, airports_file):
    """
    return two most connected cities from flights database.
    """
    with open(flights_file) as flights:
        connected_airports_frequency = dict()
        flights_reader = csv.DictReader(flights)
        for line in flights_reader:
            if (line["origin"], line["dest"]) not in connected_airports_frequency:
                connected_airports_frequency[(line["origin"], line["dest"])] = 1
            connected_airports_frequency[(line["origin"], line["dest"])] += 1
        most_connected_airports = sorted(
            connected_airports_frequency.items(), key=lambda item: item[1]
        )[-1]
    two_most_connected_cities = []
    with open(airports_file) as airports:
        airports_reader = csv.DictReader(airports)
        for line in airports_reader:
            for airport in most_connected_airports[0]:
                if airport == line["IATA_CODE"]:
                    two_most_connected_cities.append(line["CITY"])
    return two_most_connected_cities


if __name__ == "__main__":
    print(total_number_of_days("flights.csv"))  # Output = 365
    print(
        departure_cities("flights.csv", "airports.csv")
    )  # Output = {'New York', 'Newark'}
    print(relationship("flights.csv", "planes.csv"))  # Output = ['year', 'tailnum']
    print(
        manufacturer_with_most_delays("flights.csv", "planes.csv")
    )  # Output = EMBRAER
    print(
        two_most_connected_cities("flights.csv", "airports.csv")
    )  # Output = ['New York', 'Los Angeles']