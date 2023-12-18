
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