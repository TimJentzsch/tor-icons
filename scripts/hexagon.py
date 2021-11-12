#!/usr/bin/env python3
from typing import List, Optional, Tuple
import math
import numpy as np


Point = Tuple[float, float]
Polygon = List[Point]


def get_circle_point(radius: float, angle: float, center: Point = (0, 0)) -> Point:
    """Get a point on a circle."""
    cx, cy = center
    x = cx + radius * math.sin(angle)
    y = cy + radius * math.cos(angle)
    return x, y


def get_hexagon_points(radius: float, center: Point = (0, 0)) -> List[Point]:
    """Get the points of a hexagon."""
    return np.array(
        [get_circle_point(radius, p * (math.pi / 3), center) for p in range(0, 6)]
    )


def get_outer_rectangles(hexagon: Polygon, width: float) -> List[Polygon]:
    """Get the outer rectangles of an expanded hexagon structure."""
    # Three rectangles for each hexagon
    rects: List[Polygon] = []

    for i in range(0, 6):
        one, two = (np.array(hexagon[i]), np.array(hexagon[(i + 1) % 6]))
        dx, dy = two - one
        vec = np.array([-dy, dx])
        # Resize to width
        vec = vec / np.sqrt(np.sum(vec ** 2)) * width
        three = two + vec
        four = one + vec
        rects.append(np.array([one, two, three, four]))

    return rects


def get_outer_triangles(hexagon: Polygon, rectangles: List[Polygon]) -> List[Polygon]:
    """Get the outer triangles of an expanded hexagon structure."""
    triangles: List[List[Point]] = []

    for i in range(0, 6):
        one = hexagon[i]
        two = rectangles[i][3]
        three = rectangles[(i + 5) % 6][2]

        triangles.append(np.array([one, two, three]))

    return triangles


def get_expanded_hexagon_structure(
    radius: float, border_size: float, center: Point = (0, 0)
):
    hexagon = get_hexagon_points(radius - border_size, center)
    rectangles = get_outer_rectangles(hexagon, border_size)
    triangles = get_outer_triangles(hexagon, rectangles)

    return hexagon, rectangles, triangles


def points_to_svg_data(points: Polygon) -> str:
    """Convert a list of points to a SVG string."""
    return " ".join([f"{round(x, 3)},{round(y, 3)}" for (x, y) in points])


def points_to_svg_polygon(points: Polygon, class_name: Optional[str] = None) -> str:
    data = points_to_svg_data(points)
    if class_name:
        return f'<polygon class="{class_name}" points="{data}" />'
    else:
        return f'<polygon points="{data}" />'


if __name__ == "__main__":
    hexagon, rectangles, triangles = get_expanded_hexagon_structure(50, 20, (50, 50))

    print("<!-- Outer Rectangles -->")
    for rect in rectangles:
        print(points_to_svg_polygon(rect, "shade-3"))
    print("<!-- Outer Triangles -->")
    for tri in triangles:
        print(points_to_svg_polygon(tri, "shade-1"))
    print("<!-- Inner Hexagon -->")
    print(points_to_svg_polygon(hexagon, "shade-2"))
