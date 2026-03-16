Midterm Lab 2: Shortest Path and Node Routing
=============================================

Project Overview
----------------

This assignment implements a routing system based on the provided Cavite node map. It calculates the most efficient path between two selected towns. The user can choose to optimize their route based on Distance (km), Time (mins), or Fuel (Liters).

How to Run the Program
----------------------

This project was developed as a frontend web application for better interactivity.

1.  Extract the files and locate index.html.
    
2.  Open index.html using any standard web browser.
    
3.  Use the dropdown menus to select your starting location, destination, and preferred optimization metric, then click calculate.
    

Development Approach
--------------------

*   **Data Representation**: The table from the instructions was converted into a directed graph format using JavaScript objects.
    
*   **Visualization Tool**: To satisfy the node map requirement, the vis-network library was integrated. This renders an interactive, draggable network map on the screen.
    
*   **Styling**: Tailwind CSS was utilized to quickly style the user interface and create a clean layout for the controls and result outputs.
    

Algorithm Selection
-------------------

The application uses **Dijkstra's Algorithm** to determine the optimal route.

*   **Reason for choice**: Dijkstra's algorithm is ideal for finding the shortest path in graphs with non-negative weights.
    
*   **Implementation**: The algorithm was written to dynamically accept a weight parameter (distance, time, or fuel). This allows a single function to calculate the path regardless of what the user selects in the dropdown menu, making the code much more efficient.
    

Challenges Encountered
----------------------

1.  **Handling One-Way vs Two-Way Routes**: Translating the table into a graph required careful attention to direction. Since the data explicitly listed "From" and "To" nodes, the graph had to be strictly directed.
    
2.  **Dynamic Weights**: Modifying the standard Dijkstra algorithm to accept dynamic criteria instead of a hardcoded weight value took some trial and error.
    
3.  **Map Interaction**: Connecting the output of the algorithm (an array of nodes) to the visualization library to make the path change color required mapping the specific edge IDs back to the visual interface.