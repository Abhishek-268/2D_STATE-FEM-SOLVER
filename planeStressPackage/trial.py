import pyvista as pv
import numpy as np


def calculate_quad_size(quad_points):
    """Calculate a representative size for the quad element."""
    # Example: Use the length of the first side of the quad
    side_length = np.linalg.norm(quad_points[1] - quad_points[0])
    return side_length


def create_scaled_triangle(base_length, center_point):
    """Create a triangle scaled according to the base_length and positioned at the center_point."""
    height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle

    # Define the triangle vertices (centered around the origin initially)
    triangle_points = np.array([
        [-base_length / 2, 0.0, 0.0],  # Left vertex
        [base_length / 2, 0.0, 0.0],  # Right vertex
        [0.0, height, 0.0]  # Top vertex
    ])

    # Translate triangle to the center point
    triangle_points += center_point

    # Define the connectivity of the triangle
    faces = np.array([[3, 0, 1, 2]])  # Single triangle face

    return pv.PolyData(triangle_points, faces)


# Example: Define a quad element
quad_points = np.array([
    [0.0, 0.0, 0.0],  # Bottom-left
    [2.0, 0.0, 0.0],  # Bottom-right
    [2.0, 2.0, 0.0],  # Top-right
    [0.0, 2.0, 0.0]  # Top-left
])

# Calculate the size of the quad element (e.g., based on the first side)
quad_size = calculate_quad_size(quad_points)

# Create a scaled triangle at one of the quad's vertices (or any point of interest)
constraint_triangle = create_scaled_triangle(quad_size * -0.3, quad_points[0])  # Scaling factor of 0.3

# Create a PolyData object for the quad element
quad_faces = np.array([[4, 0, 1, 2, 3]])
quad_mesh = pv.PolyData(quad_points, quad_faces)

# Visualization
plotter = pv.Plotter()
plotter.add_mesh(quad_mesh, color='blue', show_edges=True)
plotter.add_mesh(constraint_triangle, color='red', show_edges=True)

plotter.set_background("white")
plotter.show()