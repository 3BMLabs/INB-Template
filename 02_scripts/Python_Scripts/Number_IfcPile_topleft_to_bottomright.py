import ifcopenshell
import ifcopenshell.util.placement
import time
start_time = time.time()


# Specify the path to your IFC file
ifc_file_path = "" # Change \ to /
file_path = ifc_file_path.removesuffix(".ifc")

# Open the IFC file
ifc_file = ifcopenshell.open(ifc_file_path)

# Initialize a list to store the coordinates and corresponding IfcPile objects
coordinates = []

# Loop through all IfcPile elements
for pile in ifc_file.by_type('IfcPile'):
    # Extract the placement (location) for the pile
    if pile.ObjectPlacement:
        matrix = ifcopenshell.util.placement.get_local_placement(pile.ObjectPlacement)
        # The location is stored in the last column of the matrix
        location = matrix[:, 3][:3]  # Get x, y, z coordinates
        coordinates.append((location[0], location[1], pile))  # Store x, y, and the IfcPile element

# Sort the coordinates from top-left to bottom-right (highest y first, lowest x second)
sorted_coordinates = sorted(coordinates, key=lambda p: (-p[1], p[0]))

# Set the starting number for numbering
start_number = 1  # You can change this value to whatever starting number you want

# Number the sorted IfcPile elements
for i, (x, y, pile) in enumerate(sorted_coordinates):
    # Create the tag (number) for the pile
    tag_value = str(start_number + i)
    
    # Assign the tag value to the pile's 'Tag' attribute (if it exists)
    if hasattr(pile, 'Tag'):
        pile.Tag = tag_value
        print(f"Updated {pile.GlobalId} with Tag: {tag_value}")
    else:
        print(f"Error: 'Tag' attribute not found for {pile.GlobalId}")
    
#Optionally, save the updated IFC file under a new name
ifc_file.write(file_path + "_numbered.ifc")
print("IFC Saved to: ", file_path + "_numbered.ifc")
print("--- %s seconds ---" % (time.time() - start_time))