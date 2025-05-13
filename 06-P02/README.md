# Delaunay Triangulation: From Points to Meshes

**Author:** Arun Soma
**Course:** 5243 Advanced Algorithms
**Date:** April 24, 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Triangulation Basics](#triangulation-basics)
3. [Delaunay Triangulation](#delaunay-triangulation)
4. [Voronoi Duality](#voronoi-duality)
5. [Core Construction Algorithms](#core-construction-algorithms)

   * [Bowyer–Watson](#bowyer–watson)
   * [Divide & Conquer](#divide--conquer)
   * [Sweep Line (Fortune)](#sweep-line-fortune)
   * [Edge-Flip Restoration](#edge-flip-restoration)
6. [Data Structures & Complexity](#data-structures--complexity)
7. [Implementation Overview](#implementation-overview)
8. [Applications](#applications)
9. [Summary](#summary)
10. [Questions & MCQs](#questions--mcqs)
11. [References](#references)

---

## Introduction

Many computational tasks—like rendering, finite-element methods (FEM), and interpolation—require a high-quality mesh. Without a good triangulation, you can get “sliver” triangles that cause numerical instability or poor convergence. Delaunay triangulation maximizes the minimum angle across all triangles, ensuring more well-shaped meshes.

## Triangulation Basics

* **Definition:** Given a planar set of points, a triangulation connects points to form non-overlapping triangles covering the convex hull.
* **Properties:** Any two triangles share at most one edge or vertex, and multiple valid triangulations can exist for the same point set.
* **Pitfalls of Naïve Meshes:** Skinny or sliver triangles lead to instability in simulations and poor interpolation quality.

## Delaunay Triangulation

* **Empty-circle property:** The circumcircle of each triangle contains no other input points in its interior.
* **Uniqueness:** When no four points are cocircular, the Delaunay triangulation is unique.
* **Max–min angle:** Among all triangulations, it maximizes the smallest angle, avoiding skinny triangles.

## Voronoi Duality

* The Voronoi diagram partitions the plane into regions of nearest neighbors.
* **Dual graph:** Connect two sites with an edge in the Delaunay triangulation if their Voronoi cells share a boundary.

## Core Construction Algorithms

### Bowyer–Watson

1. Start with a super-triangle containing all points.
2. For each new point P:

   * Find all “bad” triangles whose circumcircles contain P.
   * Extract the boundary edges of this cavity (edges seen only once).
   * Remove bad triangles and retriangulate by connecting P to each boundary edge.

### Divide & Conquer

1. Split the point set in half.
2. Recursively build Delaunay triangulations on each subset.
3. Merge the two triangulations into a single Delaunay triangulation.

### Sweep Line (Fortune’s Algorithm)

1. Move a line (the “beach line”) across the plane.
2. Maintain a dynamic structure of partial Voronoi edges.
3. Update as events (site and circle events) occur.

### Edge-Flip Restoration

1. Begin with any triangulation of the point set.
2. Repeatedly flip edges that violate the empty-circle property until no violations remain.

## Data Structures & Complexity

* **Points:** Array of (x, y) coordinates.
* **Triangles:** List of index triples referring to the point array.
* **Circumcircle tests:** Computed on demand (no caching).
* **Complexity:** Bowyer–Watson is $O(n^2)$ worst-case per insertion; expected $O(n \log n)$ with randomized input.

## Implementation Overview

* Reference implementations often follow Bowyer–Watson for simplicity.
* Key steps:

  1. Data input and super-triangle creation.
  2. Incremental insertion loop.
  3. Cavity detection and edge extraction.
  4. Retriangulation and cleanup.

## Applications

* **Mesh generation** for FEM/FVM.
* **Scattered-data interpolation** (natural neighbor interpolation, barycentric methods).
* **Computer graphics:** terrain modeling, remeshing, collision detection.
* **Geospatial analysis & sensor networks:** coverage, connectivity modeling.

## Summary

Delaunay triangulation provides a robust way to generate high-quality meshes by maximizing the minimum angle and ensuring no point lies inside any triangle’s circumcircle. Multiple algorithms exist—each with tradeoffs in complexity and implementation difficulty.

## Questions & MCQs

1. **MCQ:** Which property defines a Delaunay triangulation?
   A. Every triangle’s circumcircle contains no other points.
   B. Every triangle maximizes area.
   C. Every edge is shortest possible.
   D. Each point lies on at least one circumcircle.
   **Answer:** A

2. **MCQ:** What optimality guarantee does Delaunay triangulation provide?
   A. Minimizes number of triangles.
   B. Maximizes smallest angle.
   C. Minimizes sum of squared edges.
   D. Produces equilateral triangles.
   **Answer:** B

3. **MCQ:** Which algorithm builds a Delaunay triangulation in expected $O(n \log n)$ time?
   A. Graham-scan insertion.
   B. Bowyer–Watson incremental.
   C. Quickhull.
   D. Kruskal’s MST.
   **Answer:** B

4. **Fill in the Blank:** The Bowyer–Watson algorithm starts with a \_\_\_\_\_-triangle that contains all input points.

5. **Fill in the Blank:** The Voronoi diagram is the \_\_\_\_\_ of the Delaunay triangulation.

## References

1. Bowyer–Watson algorithm explained: [https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/](https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/)
2. Fortune’s algorithm overview: [https://www.youtube.com/watch?v=IqdSdbxrTsY\&t=90s](https://www.youtube.com/watch?v=IqdSdbxrTsY&t=90s)

