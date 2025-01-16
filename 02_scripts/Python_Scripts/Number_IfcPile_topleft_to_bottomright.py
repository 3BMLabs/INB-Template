# need to:
# 	Automatic profile retrieval and input
# 	Correct order of line making
# 	No duplicated vertices
# 	Fill in the end
# 	Support for holes
# 	Remove all error warnings


import bpy
import bmesh
import ifcopenshell
import bonsai
import bonsai.tool as tool
from mathutils import Vector

def get_curve_points(curve, model):
    """
    Extract points from IfcIndexedPolyCurve using IfcCartesianPointList2D.

    Args:
        curve: IfcIndexedPolyCurve object.
        model: The active IFC model.

    Returns:
        List of 3D points (x, y, z).
    """
    try:
        # Directly access the point list without additional checks
        point_list = model.by_id(curve.Points.id())
        return [(coord[0], coord[1], 0) for coord in point_list.CoordList]
    except AttributeError:
        return []

def round_points(points, decimals=5):
    """
    Round each point's coordinates to the specified number of decimal places.

    Args:
        points: List of 3D points (x, y, z).
        decimals: Number of decimal places to round to.

    Returns:
        List of rounded 3D points.
    """
    factor = 10**decimals
    return [(round(x * factor) / factor, round(y * factor) / factor, round(z * factor) / factor) for (x, y, z) in points]

# Main execution
if __name__ == "__main__":
    # Initialize the list to store points
    extracted_points = []

    # Get the active IFC model
    model = tool.Ifc.get()

    # The profile curve ID (replace with correct ID)
    profile_curve_id = 4497
    profile_curve = model.by_id(profile_curve_id)

    # Extract points from the IFC curve
    if profile_curve and hasattr(profile_curve, "Points"):
        points = get_curve_points(profile_curve, model)
        extracted_points.extend(points)  # Append the extracted points to the list

    # Print the extracted points
    print("Extracted Points (before scaling):", extracted_points)

    if extracted_points:
        # Apply the scaling factor (0.001) to each point
        scaled_points = [(x * 0.001, y * 0.001, z * 0.001) for (x, y, z) in extracted_points]

        # Round the points to 5 decimals
        rounded_scaled_points = round_points(scaled_points, decimals=5)

        print("Rounded Scaled Points:", rounded_scaled_points)

        # Ensure edit mode in Blender
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        # Get the active object's BMesh
        bm = bmesh.from_edit_mesh(bpy.context.object.data)

        # Create vertices all at once
        verts = [bm.verts.new(Vector(point)) for point in rounded_scaled_points]

        # Create edges all at once by iterating over the vertices
        for i in range(len(verts) - 1):
            bm.edges.new((verts[i], verts[i + 1]))

        # Close the loop by connecting the last vertex to the first one (v0)
        bm.edges.new((verts[-1], verts[0]))

        # Update the mesh once after all operations
        bmesh.update_edit_mesh(bpy.context.object.data)

        print("Mesh generated with vertices and edges.")
    else:
        print("No points were extracted from the profile curve.")
