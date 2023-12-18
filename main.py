import math
import time
import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M = 5.972e24  # Mass of the Earth (kg)
R = 6371000  # Radius of the Earth (m)
coefficient = 2.2 #sample drag coefficient of satellite
cross_area = 10 #sample surface cross sectional area of satellite (m^2)
data = []


#separate function to process the data
def calculations(height, mass, drag_coefficient, cross_sectional_area): 
    # Calculate gravitational force 
    gravitational_force = (G * M * mass) / (R + height)**2
    # Calculate satellite speed
    satellite_speed = math.sqrt(gravitational_force / mass)
    # Calculate satellite period
    satellite_period = 2 * math.pi * math.sqrt((R + height)**3 / (G * M))
    # Calculate atmospheric density (assuming simple linear model)
    atmospheric_density = 1.225 * math.exp(-height / 8200)
    # Calculate drag force
    drag_force = 0.5 * drag_coefficient * cross_sectional_area * atmospheric_density * satellite_speed**2
    # Calculate acceleration due to atmospheric drag
    acceleration_drag = drag_force / mass
    # Calculate change in altitude (assuming no other forces)
    change_in_altitude = -satellite_speed * math.sin(math.pi/2) - (acceleration_drag / (2 * math.pi / satellite_period)) * math.cos(math.pi/2)

    return (height, mass, drag_coefficient, cross_sectional_area, gravitational_force, satellite_speed, satellite_period, atmospheric_density, drag_force, acceleration_drag, change_in_altitude)


#function to enter data, process them, print them and add them to the data table
def calculate_satellite_parameters():
    # User input
    height = float(input("Enter the height of the satellite (in meters): "))
    mass = float(input("Enter the mass of the satellite (in kg): "))
    drag_coefficient = float(input("Enter the drag coefficient of the satellite (default: 2.2): ") or coefficient)
    cross_sectional_area = float(input("Enter the cross-sectional area of the satellite (default: 10): ") or cross_area)

    #Calculations
    results = calculations(height, mass, drag_coefficient, cross_sectional_area)
    gravitational_force = results[4]
    satellite_speed = results[5]
    satellite_period = results[6]
    atmospheric_density = results[7]
    drag_force = results[8]
    acceleration_drag = results[9]
    change_in_altitude = results[10]

    # Print the results and add the data for this satellite
    print("Gravitational Force: {:.2f} N".format(gravitational_force))
    print("Satellite Speed: {:.2f} m/s".format(satellite_speed))
    print("Satellite Period: {:.2f} seconds".format(satellite_period))
    #print("Atmospheric Density: " + str(atmospheric_density) + " kg/m^3")
    print("Atmospheric Density: {:.2f} kg/m^3".format(atmospheric_density))
    print("(" + str(atmospheric_density) + ")")
    print("Drag Force: {:.2f} N".format(drag_force))
    print("(" + str(drag_force) + ")")
    print("Acceleration due to Atmospheric Drag: {:.2f} m/s^2".format(acceleration_drag))
    print("(" + str(acceleration_drag) + ")")
    print("Change in Altitude: {:.2f} m/s".format(change_in_altitude))
    data.append((height, mass, drag_coefficient, cross_sectional_area, gravitational_force, satellite_speed, satellite_period, atmospheric_density, drag_force, acceleration_drag, change_in_altitude))
    return


#sample data entry
data.append(calculations(400000, 5, 2.2, 1)) #nanosat
data.append(calculations(600000, 50, 2.2, 5)) #microsat
data.append(calculations(800000, 250, 2.2, 7)) #minisat
data.append(calculations(500000, 500, 2.2, 10))
data.append(calculations(600000, 650, 2.2, 10)) #smallsat
data.append(calculations(781000, 689, 2.2, 12)) #Iridium (communications)
data.append(calculations(535000, 12200, 2.2, 20)) #Hubble
data.append(calculations(408000, 450000, 2.2, 150)) #ISS


#function to create sample graphs
def make_graphs():
    heights = []
    masses = []
    speeds = []
    periods = []
    drag_forces = []
    acceleration_drags = []
    altitude_changes = []
    for satellite in data:
        heights.append(satellite[0])
        masses.append(satellite[1])
        speeds.append(satellite[5])
        periods.append(satellite[6])
        drag_forces.append(satellite[8])
        acceleration_drags.append(satellite[9])
        altitude_changes.append(satellite[10])
  
    plt.plot(masses, speeds, 'bo')
    plt.xlabel('Mass (kg)')
    plt.ylabel('Speed (m/s)')
    plt.title('Satellite Speed vs Mass')
    plt.show()

    plt.plot(heights, speeds, 'go')
    plt.xlabel('Height (m)')
    plt.ylabel('Speed (m/s)')
    plt.title('Satellite Speed vs Orbit Height')
    plt.show()

    plt.plot(drag_forces, speeds, 'ro')
    plt.xlabel('Drag force (N)')
    plt.ylabel('Speed (m/s)')
    plt.title('Satellite Speed vs Drag force')
    plt.show()

    plt.plot(drag_forces, heights, 'yo')
    plt.xlabel('Drag force (N)')
    plt.ylabel('Height (m)')
    plt.title('Satellite Height vs Drag force')
    plt.show()

    plt.plot(altitude_changes, heights, 'yo')
    plt.xlabel('Altitude change (m/s)')
    plt.ylabel('Height (m)')
    plt.title('Satellite Altitude change vs Height')
    plt.show()
    

#delete data function
def delete_data():
    data.clear()

def calculate_heights(time_values, height, drag_coeff, cross_area, mass):
    # Calculate heights for each time value
    heights = [height]
    i = 0;
    delta_t = 0.5 #s
  
    while heights[i] > 0:
        speed = np.sqrt(G * M / (R + heights[i]))
        atmospheric_density = 1.225 * math.exp(-heights[i] / 8200)
        drag_force = 0.5 * drag_coeff * cross_area * atmospheric_density * speed ** 2
        acceleration_drag = -drag_force / mass
        delta_h = -speed * delta_t + 0.5 * acceleration_drag * delta_t ** 2

        # Calculate height
        new_height = heights[i] + delta_h
        heights.append(new_height)
        time_values.append(time_values[i] + delta_t)
        i = i +1

    return heights

def create_time_graph():
    # Sample time values and altitude values
    time_values = [0]
    height = data[0][0]
    mass = data[0][1]
    drag_coeff = data[0][2]
    cross_area = data[0][3]
    # Calling the function to calculate heights
    heights = calculate_heights(time_values, height, drag_coeff, cross_area, mass)
    # Printing the calculated heights
    for t, h in zip(time_values, heights):
        print("At time", t, "seconds, the height is", h, "meters")
    
    plt.plot(time_values, heights)
    plt.xlabel('Time Elapsed (s)')
    plt.ylabel('Height (m)')
    plt.title('Satellite Height vs Time')
    plt.show()


#main programm sequence run
while True:
    print("")
    time.sleep(1)
    print("Please select an option:")
    print("1. Enter data, calculate values, and print them")
    print("2. Print graphs")
    print("3. Create time - height graph")
    print("4. Print all data")
    print("5. Delete data values")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    
    if choice == "1":
        calculate_satellite_parameters()
    elif choice == "2":
        make_graphs()
    elif choice == "3":
        create_time_graph()
    elif choice == "4":
        print(data)
    elif choice == "5":
        delete_data()
    elif choice == "6":
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
print("Program end")