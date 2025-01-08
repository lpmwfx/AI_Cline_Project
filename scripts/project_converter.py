#!/usr/bin/env python3

import sys
import os
import re
import yaml
import argparse
from typing import Dict, List, Optional, Tuple

class ProjectConverter:
    def __init__(self):
        self.MAX_TOKENS_PER_TASK = 40000
        self.REQUIRED_SECTIONS = [
            "Overview",
            "Features/Components",
            "Requirements",
            "Technical Specifications",
            "Dependencies",
            "Implementation Details"
        ]

    def estimate_tokens(self, text: str) -> int:
        """Rough estimation of tokens based on text length."""
        # Approximate token count (rough estimate: 4 chars per token)
        return len(text) // 4

    def parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)
                
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return sections

    def extract_project_info(self, content: str) -> Tuple[str, str, str]:
        """Extract project name, description, and version."""
        lines = content.split('\n')
        project_name = ""
        version = "1.0.0"  # Default version
        
        for line in lines:
            if line.startswith('# '):
                project_name = line[2:].strip().strip('[]')
                break
                
        # Try to find version in content
        version_match = re.search(r'\[Version:\s*([^\]]+)\]', content)
        if version_match:
            version = version_match.group(1)
            
        return project_name, version

    def parse_features(self, features_section: str) -> List[Dict]:
        """Parse features section into structured tasks."""
        tasks = []
        current_feature = None
        feature_pattern = re.compile(r'### Feature \d+: (.+)')
        
        for line in features_section.split('\n'):
            if match := feature_pattern.match(line):
                if current_feature:
                    tasks.append(current_feature)
                feature_name = match.group(1).strip()
                current_feature = {
                    'id': f"TASK-{len(tasks) + 1}",
                    'name': f"{feature_name} Implementation",
                    'description': f"Implementation of {feature_name}",
                    'components': [feature_name.replace(' ', '')],
                    'sub_tasks': []
                }
            elif current_feature and line.strip().startswith('- Sub-feature'):
                # Extract sub-feature details
                sub_feature_match = re.match(r'\s*- Sub-feature (\d+\.\d+): (.+)', line)
                if sub_feature_match:
                    sub_id, sub_name = sub_feature_match.groups()
                    sub_task = {
                        'id': f"TASK-{sub_id}",
                        'name': f"Sub-feature {sub_id}",
                        'description': sub_name.strip(),
                        'estimated_tokens': 25000,  # Default estimation
                        'dependencies': [],
                        'status': 'pending'
                    }
                    current_feature['sub_tasks'].append(sub_task)
                    
        if current_feature:
            tasks.append(current_feature)
            
        return tasks

    def validate_requirements(self, sections: Dict[str, str]) -> List[str]:
        """Validate that all required sections are present and not empty."""
        errors = []
        
        # Check for required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in sections:
                errors.append(f"Missing required section: {section}")
            elif not sections[section].strip():
                errors.append(f"Empty required section: {section}")
                
        # Check for features
        if "Features/Components" in sections:
            features_content = sections["Features/Components"]
            if not re.search(r'### Feature \d+:', features_content):
                errors.append("No features found in Features/Components section")
                
        return errors

    def generate_yaml(self, markdown_path: str) -> Tuple[Dict, List[str]]:
        """Generate YAML structure from markdown file."""
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return None, [f"Error reading file: {str(e)}"]

        # Parse sections
        sections = self.parse_markdown_sections(content)
        
        # Validate requirements
        errors = self.validate_requirements(sections)
        if errors:
            return None, errors

        # Extract project info
        project_name, version = self.extract_project_info(content)
        
        # Parse features into tasks
        tasks = self.parse_features(sections.get("Features/Components", ""))
        
        # Create YAML structure
        yaml_structure = {
            'project': {
                'name': project_name,
                'description': sections.get("Overview", "").strip(),
                'version': version
            },
            'tasks': tasks,
            'settings': {
                'max_tokens_per_task': self.MAX_TOKENS_PER_TASK,
                'default_status': 'pending',
                'allowed_statuses': [
                    'pending',
                    'in_progress',
                    'completed',
                    'blocked'
                ]
            },
            'task_files': []
        }
        
        # Add task files references
        for task in tasks:
            component = task['components'][0]
            yaml_structure['task_files'].append({
                'path': f"src/libs/{component}/task_{component}.yaml",
                'tasks': [subtask['id'] for subtask in task['sub_tasks']]
            })
        
        return yaml_structure, []

def main():
    parser = argparse.ArgumentParser(description='Convert project markdown to YAML')
    parser.add_argument('input', help='Input markdown file path')
    parser.add_argument('--output', '-o', help='Output YAML file path')
    args = parser.parse_args()

    converter = ProjectConverter()
    yaml_structure, errors = converter.generate_yaml(args.input)

    if errors:
        print("Errors found:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or os.path.splitext(args.input)[0] + '.yaml'
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_structure, f, default_flow_style=False, sort_keys=False)
        print(f"Successfully converted to {output_path}")
    except Exception as e:
        print(f"Error writing YAML file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
