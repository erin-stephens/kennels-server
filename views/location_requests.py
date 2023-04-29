import sqlite3
import json
from models import Location, Employee, Animal, Customer

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    '''gets all the locations'''
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM Location l
        """)

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # location class above.
            location = Location(row['id'], row ['name'], row['address'])

            locations.append(location.__dict__)
            # see the notes below for an explanation on this line of code.

    return locations

# Function with a single parameter
def get_single_location(id):
    '''gets single location'''
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM Location l
        WHERE l.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an location instance from the current row
        location = Location(data['id'], data['name'] ,data['address'])

        db_cursor2 = conn.cursor()
        db_cursor2.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM Animal a
            WHERE location_id = ?
            """, ( id, ))
        animals = []
        dataset2 = db_cursor2.fetchall()
        for row in dataset2:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                                row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)
            location.animal = animals

        db_cursor3 = conn.cursor()
        db_cursor3.execute("""
            SELECT
            c.id,
            c.name,
            c.address,
            c.location_id
        FROM employee c
            WHERE location_id = ?
            """, ( id, ))
        employees = []
        dataset3 = db_cursor3.fetchall()
        for row in dataset3:
            employee = Employee(row['id'], row['name'], row['location_id'], row['address'])
            employees.append(employee.__dict__)
            location.employee = employees
    return location.__dict__

def create_location(location):
    '''makes a new location'''
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the location dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    '''deletes location'''
    # Initial -1 value for location index, in case one isn't found
    location_index = -1

    # Iterate the locationS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the location was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)

def update_location(id, new_location):
    '''updates location'''
    # Iterate the locationS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Update the value.
            LOCATIONS[index] = new_location
            break
