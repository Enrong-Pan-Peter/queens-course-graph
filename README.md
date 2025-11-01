# Queen's University Course Prerequisites Graph Visualizer

An interactive force-directed graph visualization showing course prerequisites and relationships for Mathematics, Statistics, and Computing courses at Queen's University.

## Overview

This project visualizes the prerequisite relationships between courses at Queen's University using a physics-based force-directed graph. The visualization helps students understand course dependencies and plan their academic progression.

## Features

### Interactive Visualization
- **Physics-Based Layout**: Uses Hooke's Law (spring forces) and Coulomb's Law (repulsion) to naturally organize courses
- **Zoom & Pan**: Fully interactive canvas with mouse wheel zoom and drag-to-pan
- **Hover Effects**: Hover over nodes to see detailed course information
- **Connection Highlighting**: Automatically highlights prerequisite chains when hovering

### Filtering & Search
- **Subject Filters**: Filter by MATH, STAT, or CISC courses
- **Search**: Real-time search by course code or name
- **Reset View**: One-click reset to default view

### Visual Design
- **Morandi Color Palette**: Warm, muted colors for visual comfort
  - Mathematics (MATH): Dusty terracotta (#D4A574)
  - Statistics (STAT): Muted sage green (#A8B5A0)
  - Computing (CISC): Dusty blue-grey (#9BADB7)
- **Node Sizing**: Proportional to credit units (3.0 = smaller, 6.0 = larger)
- **Isolated Nodes**: Courses without prerequisites shown with reduced opacity
- **Clean UI**: Greyish-white background (#F5F5F3) for minimal distraction

## Data Statistics

- **Total Courses**: 96
  - MATH: 48 courses
  - STAT: 16 courses
  - CISC: 32 courses
- **Total Prerequisites**: 113 relationships
- **Connected Components**: 14 (includes isolated courses)
- **Largest Component**: 54 interconnected courses
- **Isolated Courses**: 10 (e.g., MATH 499, CISC 499, thesis courses)

## How to Use

### Opening the Visualization
1. Open `index.html` in a modern web browser (Chrome, Firefox, Safari, Edge)
2. The graph will load automatically and begin its physics simulation
3. Wait a few seconds for the layout to stabilize

### Navigation
- **Zoom**: Use mouse wheel or trackpad pinch
- **Pan**: Click and drag on empty space
- **Move Nodes**: Click and drag individual nodes
- **View Details**: Hover over any course node

### Filtering
- Click **MATH**, **STAT**, or **CISC** buttons to filter by subject
- Click again to toggle filter off
- Use the **Search** box to find specific courses
- Click **Reset View** to clear all filters and reset zoom

### Reading the Graph
- **Arrows**: Point from prerequisite → to dependent course
- **Node Size**: Larger nodes = more credit units
- **Node Color**: Indicates subject area (see legend)
- **Opacity**: Faded nodes = isolated courses (no prerequisites)
- **Connections**: Lines show direct prerequisite relationships

## Technical Implementation

### Physics Simulation Parameters
```javascript
// Hooke's Law (Spring Force)
- Link Distance: 120px (rest length)
- Link Strength: 0.5 (spring constant)

// Coulomb's Law (Repulsion)
- Charge Strength: -500 (repulsion force)
- Collision Radius: nodeSize + 5px

// Damping
- Alpha Decay: 0.02 (friction/damping coefficient)
```

### Technology Stack
- **D3.js v7**: Force simulation and SVG rendering
- **Vanilla JavaScript**: No framework dependencies
- **HTML5 Canvas/SVG**: Vector graphics for scalability
- **Python**: Data extraction and graph construction

### File Structure
```
├── index.html          # Main visualization interface
├── graph.json          # Course graph data (nodes & edges)
├── courses.json        # Raw course data with metadata
├── scraper.py          # Data extraction script
└── build_graph.py      # Graph structure builder
```

## Data Source

All course data is sourced from the Queen's University Academic Calendar 2025-2026:
- [Mathematics Course Descriptions](https://www.queensu.ca/academic-calendar/arts-science/course-descriptions/math/)
- [Statistics Course Descriptions](https://www.queensu.ca/academic-calendar/arts-science/course-descriptions/stat/)
- [Computing Course Descriptions](https://www.queensu.ca/academic-calendar/arts-science/course-descriptions/cisc/)

## Graph Structure

### Nodes
Each course is represented as a node with properties:
- `id`: Unique identifier (e.g., "MATH110")
- `code`: Full course code (e.g., "MATH 110")
- `name`: Course title
- `subject`: Department (MATH/STAT/CISC)
- `units`: Credit value (3.0 or 6.0)
- `level`: Course level (100/200/300/400)
- `prerequisites`: Array of prerequisite course codes

### Edges
Prerequisite relationships are directed edges:
- `source`: Prerequisite course ID
- `target`: Dependent course ID
- `type`: "prerequisite"

### Components
The graph contains multiple connected components:
1. **Main Component** (54 courses): Core curriculum with heavy interconnection
2. **Secondary Components**: Smaller chains (e.g., CISC courses)
3. **Isolated Nodes**: Special topics, thesis courses, or foundational courses with no prerequisites

## Example Course Chains

### Mathematics Sequence
```
MATH 110 (Linear Algebra)
  → MATH 210 (Rings and Fields)
    → MATH 310 (Group Theory)
      → MATH 418 (Algebraic Geometry)
```

### Statistics Sequence
```
MATH 120 (Calculus)
  → STAT 252 (Probability)
    → STAT 353 (Probability II)
      → STAT 455 (Stochastic Processes)
```

### Computing Sequence
```
CISC 121 (Intro to Computing I)
  → CISC 124 (Intro to Computing II)
    → CISC 235 (Data Structures)
      → CISC 365 (Algorithms I)
```

## Interesting Insights

1. **Hub Courses**: MATH 110, MATH 120, and CISC 124 are critical hubs with many follow-up courses
2. **Parallel Paths**: Multiple calculus tracks (MATH 120/121/126/127) serve different programs
3. **Cross-Department Links**: STAT courses heavily depend on MATH prerequisites
4. **Terminal Courses**: Advanced 400-level courses like MATH 487 are endpoints
5. **Flexibility**: 10 isolated courses provide entry points without prerequisites

## Future Enhancements

Potential improvements for future versions:
- [ ] Add course scheduling information (Fall/Winter/Year)
- [ ] Include course difficulty ratings or workload estimates
- [ ] Show professor information and ratings
- [ ] Add corequisite relationships (dashed lines)
- [ ] Include exclusion relationships
- [ ] Export prerequisite chains as PDF/PNG
- [ ] Add "shortest path to course X" feature
- [ ] Include graduate courses (800-level)
- [ ] Show historical enrollment data
- [ ] Mobile-responsive design improvements

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

Requires JavaScript enabled and SVG support.

## Credits
 
**Data Source**: Queen's University Academic Calendar  
**Visualization Library**: D3.js  
**Design Inspiration**: Connected Papers  
**Color Palette**: Morandi warm tones  

## License

Educational use only. Course data © Queen's University.  
Visualization code is provided as-is for reference.

## Contact & Feedback

For questions about course content, contact:
- **Math & Stats Undergraduate Office**: mathstat.ugassistant@queensu.ca
- **School of Computing Advising**: advising@cs.queensu.ca

