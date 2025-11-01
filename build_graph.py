import json
from collections import defaultdict, deque

# Load course data
with open('/home/claude/data/courses.json', 'r') as f:
    data = json.load(f)

courses = data['courses']

# Build graph structure
nodes = []
edges = []
course_map = {}

# Create nodes
for course in courses:
    node = {
        'id': course['code'].replace(' ', ''),  # MATH110, CISC121, etc.
        'label': f"{course['code']}: {course['name'][:30]}",
        'fullName': course['name'],
        'code': course['code'],
        'subject': course['subject'],
        'units': course['units'],
        'level': course['level'],
        'prerequisites': course['prerequisites']
    }
    nodes.append(node)
    course_map[course['code']] = node

# Create edges (prerequisite relationships)
for course in courses:
    target_id = course['code'].replace(' ', '')
    
    for prereq in course['prerequisites']:
        if prereq in course_map:
            source_id = prereq.replace(' ', '')
            edges.append({
                'source': source_id,
                'target': target_id,
                'type': 'prerequisite'
            })

# Calculate follow-up courses (inverse relationships)
followups = defaultdict(list)
for edge in edges:
    followups[edge['source']].append(edge['target'])

# Add follow-up count to nodes
for node in nodes:
    node['followupCount'] = len(followups[node['id']])

# Find connected components using BFS
def find_components(nodes, edges):
    """Find connected components in the graph"""
    # Build adjacency list (undirected)
    adj = defaultdict(set)
    for edge in edges:
        adj[edge['source']].add(edge['target'])
        adj[edge['target']].add(edge['source'])
    
    visited = set()
    components = []
    
    for node in nodes:
        node_id = node['id']
        if node_id not in visited:
            # BFS to find component
            component = []
            queue = deque([node_id])
            visited.add(node_id)
            
            while queue:
                current = queue.popleft()
                component.append(current)
                
                for neighbor in adj[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    # Sort components by size
    components.sort(key=len, reverse=True)
    return components

components = find_components(nodes, edges)

# Categorize nodes
main_component = components[0] if components else []
isolated_nodes = [comp[0] for comp in components if len(comp) == 1]

print(f"\nGraph Structure Analysis:")
print(f"  Total nodes: {len(nodes)}")
print(f"  Total edges: {len(edges)}")
print(f"  Number of connected components: {len(components)}")
print(f"  Largest component size: {len(main_component)} nodes")
print(f"  Number of isolated nodes: {len(isolated_nodes)}")

print(f"\nComponent sizes:")
for i, comp in enumerate(components[:10]):  # Show first 10 components
    print(f"  Component {i+1}: {len(comp)} nodes")

print(f"\nIsolated courses (no prerequisites and no follow-ups):")
for node_id in isolated_nodes[:10]:  # Show first 10
    node = next(n for n in nodes if n['id'] == node_id)
    print(f"  {node['code']}: {node['fullName']}")

# Prepare graph output
graph_output = {
    'nodes': nodes,
    'edges': edges,
    'components': {
        'main': main_component,
        'isolated': isolated_nodes,
        'all': [[node_id for node_id in comp] for comp in components]
    },
    'statistics': {
        'total_nodes': len(nodes),
        'total_edges': len(edges),
        'component_count': len(components),
        'largest_component_size': len(main_component),
        'isolated_count': len(isolated_nodes)
    }
}

# Save graph data
with open('/home/claude/data/graph.json', 'w') as f:
    json.dump(graph_output, f, indent=2)

print(f"\nGraph data saved to graph.json")

# Show some statistics by subject
print(f"\nCourses by subject:")
subject_stats = defaultdict(lambda: {'total': 0, 'with_prereqs': 0, 'isolated': 0})
for node in nodes:
    subj = node['subject']
    subject_stats[subj]['total'] += 1
    if len(node['prerequisites']) > 0:
        subject_stats[subj]['with_prereqs'] += 1
    if node['id'] in isolated_nodes:
        subject_stats[subj]['isolated'] += 1

for subject in sorted(subject_stats.keys()):
    stats = subject_stats[subject]
    print(f"  {subject}: {stats['total']} total, {stats['with_prereqs']} with prerequisites, {stats['isolated']} isolated")
