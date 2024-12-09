import re
import subprocess
import sys
import os

# Check if correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python replace_plantuml.py <input_md_file> <output_folder>")
    sys.exit(1)

# File paths from command line arguments
input_file = sys.argv[1]
output_folder = sys.argv[2]

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Read the markdown file
with open(input_file, 'r') as f:
    content = f.read()

# Regex pattern to match PlantUML blocks and extract the diagram name
plantuml_pattern = re.compile(r'```plantuml\s*@startuml\s*([\w-]+)(.*?)@enduml\s*```', re.DOTALL)

# Function to replace PlantUML block with image link
def replace_plantuml_with_image(match):
    diagram_name = match.group(1).strip()  # Extract diagram name from @startuml
    image_name = f"{diagram_name}.png"
    return f'![{diagram_name}]({image_name})'

# Replace all PlantUML blocks with image references
new_content = plantuml_pattern.sub(replace_plantuml_with_image, content)

# Path for the output markdown file
output_md_file = os.path.join(output_folder, os.path.basename(input_file))

# Write the updated markdown content to the output file
with open(output_md_file, 'w') as f:
    f.write(new_content)

# Change the working directory to the output folder
original_cwd = os.getcwd()
os.chdir(output_folder)

# Extract all diagram names and their content to generate images
diagram_matches = plantuml_pattern.findall(content)
for diagram_name, plantuml_code in diagram_matches:
    diagram_name = diagram_name.strip()
    plantuml_code = f"@startuml {diagram_name}\n{plantuml_code}\n@enduml"
    plantuml_file = f"{diagram_name}.puml"
    with open(plantuml_file, 'w') as f:
        f.write(plantuml_code)
    subprocess.run(['plantuml', '-tpng', '-Ddpi=300', plantuml_file])
    os.remove(plantuml_file)

# Restore the original working directory
os.chdir(original_cwd)

print(f"Updated markdown written to {output_md_file} and PNG files generated in {output_folder}.")