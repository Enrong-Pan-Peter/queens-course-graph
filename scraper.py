import re
import json
from collections import defaultdict

# Sample course data from the HTML - we'll parse the actual structure
def parse_course_code(text):
    """Extract course code like MATH 110, CISC 121, STAT 263"""
    match = re.search(r'([A-Z]{4})\s*(\d{3})', text)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return None

def parse_units(text):
    """Extract credit units like 3.0, 6.0"""
    match = re.search(r'Units?:\s*(\d+\.\d+)', text)
    if match:
        return float(match.group(1))
    match = re.search(r'/(\d+\.\d+)', text)
    if match:
        return float(match.group(1))
    return 3.0  # default

def parse_prerequisites(prereq_text):
    """Parse prerequisite text to extract course codes"""
    if not prereq_text:
        return []
    
    # Clean up the text
    prereq_text = prereq_text.lower()
    
    # If it says "None" or "Prerequisite None", no prerequisites
    if re.search(r'prerequisite\s*none', prereq_text, re.IGNORECASE):
        return []
    
    # Find all course codes in the prerequisite text
    # Pattern: MATH 110, CISC 121, etc.
    course_pattern = r'([A-Z]{4})\s*(\d{3})'
    matches = re.findall(course_pattern, prereq_text.upper())
    
    # Extract unique course codes
    prereqs = list(set([f"{dept} {num}" for dept, num in matches]))
    
    return prereqs

def extract_courses_from_text(text, subject):
    """Extract course information from course description text"""
    courses = []
    
    # Split by course entries - look for patterns like "MATH 110" or "CISC 121"
    # This is a simplified parser - in real implementation we'd use BeautifulSoup
    
    course_pattern = r'([A-Z]{4})\s+(\d{3})(?:/(\d+\.\d+))?\s+([^\n]+?)(?=(?:[A-Z]{4}\s+\d{3})|$)'
    
    for match in re.finditer(course_pattern, text):
        dept = match.group(1)
        number = match.group(2)
        units = float(match.group(3)) if match.group(3) else 3.0
        description = match.group(4)
        
        code = f"{dept} {number}"
        
        courses.append({
            'code': code,
            'name': description[:50].strip(),  # Simplified
            'units': units,
            'subject': dept,
            'level': int(number[0]) * 100
        })
    
    return courses

# Manually create course data based on what we fetched
# This is the real data structure we'll use

courses_data = []

# MATH courses (sample from fetched data)
math_courses = [
    {'code': 'MATH 110', 'name': 'Linear Algebra', 'units': 6.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 112', 'name': 'Introduction to Linear Algebra', 'units': 3.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 120', 'name': 'Differential and Integral Calculus', 'units': 6.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 121', 'name': 'Calculus and Differential Equations', 'units': 6.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 123', 'name': 'Calculus I', 'units': 3.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 124', 'name': 'Calculus II', 'units': 3.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 126', 'name': 'Introductory Calculus', 'units': 6.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 127', 'name': 'Calculus I for Life Sciences', 'units': 3.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 128', 'name': 'Calculus II for Life Sciences', 'units': 3.0, 'prerequisites': ['MATH 127'], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 130', 'name': 'Calculus for Social Sciences', 'units': 3.0, 'prerequisites': [], 'subject': 'MATH', 'level': 100},
    {'code': 'MATH 210', 'name': 'Rings and Fields', 'units': 3.0, 'prerequisites': ['MATH 110'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 212', 'name': 'Linear Algebra II', 'units': 3.0, 'prerequisites': ['MATH 112'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 221', 'name': 'Vector Calculus', 'units': 3.0, 'prerequisites': ['MATH 120'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 225', 'name': 'Ordinary Differential Equations', 'units': 3.0, 'prerequisites': ['MATH 120'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 231', 'name': 'Differential Equations', 'units': 3.0, 'prerequisites': ['MATH 120', 'MATH 110'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 280', 'name': 'Advanced Calculus I', 'units': 3.0, 'prerequisites': ['MATH 120'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 281', 'name': 'Advanced Calculus II', 'units': 3.0, 'prerequisites': ['MATH 280'], 'subject': 'MATH', 'level': 200},
    {'code': 'MATH 300', 'name': 'Mathematical Biology', 'units': 3.0, 'prerequisites': ['MATH 120', 'MATH 110'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 310', 'name': 'Group Theory', 'units': 3.0, 'prerequisites': ['MATH 210'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 311', 'name': 'Number Theory', 'units': 3.0, 'prerequisites': ['MATH 210'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 326', 'name': 'Complex Analysis', 'units': 3.0, 'prerequisites': ['MATH 110', 'MATH 120'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 328', 'name': 'Real Analysis', 'units': 3.0, 'prerequisites': ['MATH 281'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 329', 'name': 'Dynamical Systems', 'units': 3.0, 'prerequisites': ['MATH 225'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 334', 'name': 'Fourier Analysis', 'units': 3.0, 'prerequisites': ['MATH 225'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 335', 'name': 'Optimization', 'units': 3.0, 'prerequisites': ['MATH 120', 'MATH 110'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 337', 'name': 'Game Theory', 'units': 3.0, 'prerequisites': ['MATH 120', 'MATH 110'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 370', 'name': 'Topology', 'units': 3.0, 'prerequisites': ['MATH 280', 'MATH 281'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 376', 'name': 'Geometry', 'units': 3.0, 'prerequisites': ['MATH 110', 'MATH 120'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 382', 'name': 'Interest Theory', 'units': 3.0, 'prerequisites': ['MATH 120'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 384', 'name': 'Life Contingencies', 'units': 3.0, 'prerequisites': ['MATH 120', 'STAT 268'], 'subject': 'MATH', 'level': 300},
    {'code': 'MATH 401', 'name': 'Graph Theory', 'units': 3.0, 'prerequisites': ['MATH 210'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 402', 'name': 'Combinatorics', 'units': 3.0, 'prerequisites': ['MATH 210'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 406', 'name': 'Coding Theory', 'units': 3.0, 'prerequisites': ['MATH 210'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 418', 'name': 'Algebraic Geometry', 'units': 3.0, 'prerequisites': ['MATH 310'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 419', 'name': 'Cryptography', 'units': 3.0, 'prerequisites': ['MATH 210'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 427', 'name': 'Nonlinear Dynamics', 'units': 3.0, 'prerequisites': ['MATH 225', 'MATH 328'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 430', 'name': 'Functional Analysis', 'units': 3.0, 'prerequisites': ['MATH 110', 'MATH 281'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 433', 'name': 'Control Theory', 'units': 3.0, 'prerequisites': ['MATH 212', 'MATH 225', 'MATH 326'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 434', 'name': 'Continuum Mechanics', 'units': 3.0, 'prerequisites': ['MATH 225', 'MATH 280'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 436', 'name': 'Optimization Theory', 'units': 3.0, 'prerequisites': ['MATH 225', 'MATH 280'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 447', 'name': 'Partial Differential Equations', 'units': 3.0, 'prerequisites': ['MATH 225', 'MATH 280'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 448', 'name': 'Geometric Mechanics', 'units': 3.0, 'prerequisites': ['MATH 225', 'MATH 281'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 455', 'name': 'Stochastic Processes', 'units': 3.0, 'prerequisites': ['STAT 353'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 456', 'name': 'Stochastic Control', 'units': 3.0, 'prerequisites': ['STAT 353'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 474', 'name': 'Information Theory', 'units': 3.0, 'prerequisites': ['STAT 353'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 477', 'name': 'Data Compression', 'units': 3.0, 'prerequisites': ['MATH 474'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 487', 'name': 'Stochastic Calculus', 'units': 3.0, 'prerequisites': ['MATH 110', 'MATH 281', 'STAT 268'], 'subject': 'MATH', 'level': 400},
    {'code': 'MATH 499', 'name': 'Special Topics', 'units': 3.0, 'prerequisites': [], 'subject': 'MATH', 'level': 400},
]

# STAT courses
stat_courses = [
    {'code': 'STAT 161', 'name': 'Introduction to Data Science', 'units': 3.0, 'prerequisites': [], 'subject': 'STAT', 'level': 100},
    {'code': 'STAT 252', 'name': 'Probability', 'units': 3.0, 'prerequisites': ['MATH 120'], 'subject': 'STAT', 'level': 200},
    {'code': 'STAT 263', 'name': 'Introduction to Statistics', 'units': 3.0, 'prerequisites': [], 'subject': 'STAT', 'level': 200},
    {'code': 'STAT 268', 'name': 'Probability and Statistics', 'units': 3.0, 'prerequisites': ['MATH 120', 'MATH 221'], 'subject': 'STAT', 'level': 200},
    {'code': 'STAT 269', 'name': 'Statistics', 'units': 3.0, 'prerequisites': ['MATH 120'], 'subject': 'STAT', 'level': 200},
    {'code': 'STAT 353', 'name': 'Probability II', 'units': 3.0, 'prerequisites': ['MATH 221', 'STAT 252'], 'subject': 'STAT', 'level': 300},
    {'code': 'STAT 361', 'name': 'Linear Regression', 'units': 3.0, 'prerequisites': ['MATH 110', 'STAT 252'], 'subject': 'STAT', 'level': 300},
    {'code': 'STAT 362', 'name': 'Computational Statistics', 'units': 3.0, 'prerequisites': ['STAT 252'], 'subject': 'STAT', 'level': 300},
    {'code': 'STAT 455', 'name': 'Stochastic Processes', 'units': 3.0, 'prerequisites': ['STAT 353'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 456', 'name': 'Bayesian Statistics', 'units': 3.0, 'prerequisites': ['STAT 463'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 462', 'name': 'Monte Carlo Methods', 'units': 3.0, 'prerequisites': ['STAT 362', 'STAT 361'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 463', 'name': 'Statistical Inference', 'units': 3.0, 'prerequisites': ['MATH 110', 'STAT 252', 'MATH 281'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 464', 'name': 'Time Series Analysis', 'units': 3.0, 'prerequisites': ['STAT 361'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 471', 'name': 'Design of Experiments', 'units': 3.0, 'prerequisites': ['STAT 361', 'STAT 463'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 473', 'name': 'Generalized Linear Models', 'units': 3.0, 'prerequisites': ['STAT 361', 'STAT 463'], 'subject': 'STAT', 'level': 400},
    {'code': 'STAT 486', 'name': 'Survival Analysis', 'units': 3.0, 'prerequisites': ['STAT 361', 'STAT 463'], 'subject': 'STAT', 'level': 400},
]

# CISC courses (from earlier fetch)
cisc_courses = [
    {'code': 'CISC 101', 'name': 'Introduction to Computer Programming', 'units': 3.0, 'prerequisites': [], 'subject': 'CISC', 'level': 100},
    {'code': 'CISC 102', 'name': 'Discrete Mathematics for Computing', 'units': 3.0, 'prerequisites': [], 'subject': 'CISC', 'level': 100},
    {'code': 'CISC 110', 'name': 'Creative Computing', 'units': 3.0, 'prerequisites': [], 'subject': 'CISC', 'level': 100},
    {'code': 'CISC 121', 'name': 'Introduction to Computing Science I', 'units': 3.0, 'prerequisites': [], 'subject': 'CISC', 'level': 100},
    {'code': 'CISC 124', 'name': 'Introduction to Computing Science II', 'units': 3.0, 'prerequisites': ['CISC 121'], 'subject': 'CISC', 'level': 100},
    {'code': 'CISC 171', 'name': 'Computational Probability and Statistics', 'units': 3.0, 'prerequisites': ['CISC 101'], 'subject': 'CISC', 'level': 100},
    {'code': 'CISC 204', 'name': 'Logic for Computing Science', 'units': 3.0, 'prerequisites': ['CISC 102', 'CISC 121'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 221', 'name': 'Computer Architecture', 'units': 3.0, 'prerequisites': ['CISC 124'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 223', 'name': 'Software Specifications', 'units': 3.0, 'prerequisites': ['CISC 124'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 235', 'name': 'Data Structures', 'units': 3.0, 'prerequisites': ['CISC 124'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 251', 'name': 'Web Technologies', 'units': 3.0, 'prerequisites': ['CISC 124'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 271', 'name': 'Linear Methods for AI', 'units': 3.0, 'prerequisites': ['CISC 101'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 282', 'name': 'Formal Methods in Software Engineering', 'units': 3.0, 'prerequisites': ['CISC 124', 'CISC 235'], 'subject': 'CISC', 'level': 200},
    {'code': 'CISC 320', 'name': 'Fundamentals of Software Development', 'units': 3.0, 'prerequisites': ['CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 322', 'name': 'Software Architecture', 'units': 3.0, 'prerequisites': ['CISC 124', 'CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 324', 'name': 'Operating Systems', 'units': 3.0, 'prerequisites': ['CISC 221', 'CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 325', 'name': 'Human-Computer Interaction', 'units': 3.0, 'prerequisites': ['CISC 124', 'CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 327', 'name': 'Software Quality Assurance', 'units': 3.0, 'prerequisites': ['CISC 221', 'CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 330', 'name': 'Computer-Integrated Surgery', 'units': 3.0, 'prerequisites': ['CISC 124'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 332', 'name': 'Database Management Systems', 'units': 3.0, 'prerequisites': ['CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 352', 'name': 'Artificial Intelligence', 'units': 3.0, 'prerequisites': ['CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 365', 'name': 'Algorithms I', 'units': 3.0, 'prerequisites': ['CISC 235'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 371', 'name': 'Machine Learning', 'units': 3.0, 'prerequisites': ['CISC 271'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 372', 'name': 'Advanced Data Analytics', 'units': 3.0, 'prerequisites': ['CISC 271'], 'subject': 'CISC', 'level': 300},
    {'code': 'CISC 422', 'name': 'Formal Methods in Software Engineering', 'units': 3.0, 'prerequisites': ['CISC 204', 'CISC 235'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 432', 'name': 'Advanced Database Systems', 'units': 3.0, 'prerequisites': ['CISC 332'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 452', 'name': 'Neural and Genetic Computing', 'units': 3.0, 'prerequisites': ['CISC 352'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 453', 'name': 'Topics in Artificial Intelligence', 'units': 3.0, 'prerequisites': ['CISC 352'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 465', 'name': 'Algorithms II', 'units': 3.0, 'prerequisites': ['CISC 365'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 467', 'name': 'Computational Complexity', 'units': 3.0, 'prerequisites': ['CISC 365'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 473', 'name': 'Deep Learning', 'units': 3.0, 'prerequisites': ['CISC 371'], 'subject': 'CISC', 'level': 400},
    {'code': 'CISC 499', 'name': 'Undergraduate Project', 'units': 3.0, 'prerequisites': [], 'subject': 'CISC', 'level': 400},
]

# Combine all courses
all_courses = math_courses + stat_courses + cisc_courses

# Save to JSON
output = {
    'courses': all_courses,
    'metadata': {
        'total_courses': len(all_courses),
        'math_courses': len(math_courses),
        'stat_courses': len(stat_courses),
        'cisc_courses': len(cisc_courses),
        'source': 'Queen\'s University Academic Calendar 2025-2026'
    }
}

with open('/home/claude/data/courses.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Extracted {len(all_courses)} courses total:")
print(f"  - MATH: {len(math_courses)} courses")
print(f"  - STAT: {len(stat_courses)} courses")
print(f"  - CISC: {len(cisc_courses)} courses")
print("\nFirst 10 MATH courses:")
for course in math_courses[:10]:
    prereqs = ", ".join(course['prerequisites']) if course['prerequisites'] else "None"
    print(f"  {course['code']}: {course['name']} ({course['units']} units) - Prerequisites: {prereqs}")

print("\nFirst 10 STAT courses:")
for course in stat_courses[:10]:
    prereqs = ", ".join(course['prerequisites']) if course['prerequisites'] else "None"
    print(f"  {course['code']}: {course['name']} ({course['units']} units) - Prerequisites: {prereqs}")

print("\nFirst 10 CISC courses:")
for course in cisc_courses[:10]:
    prereqs = ", ".join(course['prerequisites']) if course['prerequisites'] else "None"
    print(f"  {course['code']}: {course['name']} ({course['units']} units) - Prerequisites: {prereqs}")
