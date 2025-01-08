import yaml
import os
import re
from pathlib import Path

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def load_markdown(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def extract_section(md_content, section_title):
    pattern = rf'^#+\s*{re.escape(section_title)}\s*$'
    match = re.search(pattern, md_content, re.MULTILINE)
    if not match:
        return None
        
    start = match.start()
    next_section = re.search(r'^#+\s*[^#]', md_content[start+1:], re.MULTILINE)
    end = next_section.start() if next_section else len(md_content)
    
    return md_content[start:start+end].strip()

def create_subproject_docs(project_root, yaml_data, md_content):
    base_path = Path(project_root) / 'src' / 'libs'
    
    for task in yaml_data['tasks']:
        component = task['components'][0]
        task_ids = [sub['id'] for sub in task['sub_tasks']]
        
        # Create component-specific content
        component_content = []
        component_content.append(extract_section(md_content, 'Overview'))
        component_content.append(extract_section(md_content, task['name']))
        
        # Add relevant sections
        for section in ['Requirements', 'Technical Specifications', 'Implementation Details']:
            content = extract_section(md_content, section)
            if content:
                component_content.append(content)
        
        # Write to file
        output_path = base_path / component / f'{component}_proposal.md'
        with open(output_path, 'w') as file:
            file.write('\n\n'.join(filter(None, component_content)))

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(project_root, 'project_proposal.yaml')
    md_path = os.path.join(project_root, 'project_proposal.md')
    
    yaml_data = load_yaml(yaml_path)
    md_content = load_markdown(md_path)
    
    create_subproject_docs(project_root, yaml_data, md_content)

if __name__ == '__main__':
    main()
