#!/usr/bin/env python3

import os
import yaml
import argparse
from pathlib import Path

class ProjectInitializer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.template_dir = self.project_root / 'templates'
        self.src_dir = self.project_root / 'src'
        self.libs_dir = self.src_dir / 'libs'
        self.workflows_dir = self.src_dir / 'workflows'
        
    def create_directory_structure(self):
        """Create the base project directory structure"""
        dirs_to_create = [
            self.src_dir,
            self.libs_dir,
            self.workflows_dir,
            self.workflows_dir / 'sub_workflows',
            self.template_dir
        ]
        
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)
            
    def initialize_git(self):
        """Initialize git repository and create .gitignore"""
        gitignore_content = """# Ignore node_modules
node_modules/

# Ignore AI chat logs
ai_chatlogs/

# Ignore OS files
.DS_Store
"""
        with open(self.project_root / '.gitignore', 'w') as f:
            f.write(gitignore_content)
            
        os.system(f'cd {self.project_root} && git init')
        
    def create_component(self, component_name: str):
        """Create structure for a single component"""
        component_dir = self.libs_dir / component_name
        component_dir.mkdir(exist_ok=True)
        
        # Create component workspace file
        workspace_content = {
            'folders': [
                {'path': '.'}
            ],
            'settings': {}
        }
        with open(component_dir / f'{component_name}.code-workspace', 'w') as f:
            yaml.dump(workspace_content, f)
            
        # Create empty task file
        with open(component_dir / f'task_{component_name}.yaml', 'w') as f:
            yaml.dump({}, f)
            
        # Create ai_chatlogs directory
        (component_dir / 'ai_chatlogs').mkdir(exist_ok=True)
        
    def create_workflow_files(self, components: list):
        """Create main workflow and sub-workflows"""
        # Create main workflow
        main_workflow = {
            'name': 'Main Workflow',
            'description': 'Orchestrates all sub-workflows',
            'sub_workflows': [f'workflow_{comp}.yaml' for comp in components]
        }
        with open(self.workflows_dir / 'main_workflow.yaml', 'w') as f:
            yaml.dump(main_workflow, f)
            
        # Create sub-workflows
        for component in components:
            sub_workflow = {
                'name': f'{component} Workflow',
                'description': f'Workflow for {component} component',
                'tasks': []
            }
            with open(self.workflows_dir / 'sub_workflows' / f'workflow_{component}.yaml', 'w') as f:
                yaml.dump(sub_workflow, f)
                
    def initialize_project(self, project_config: dict):
        """Main initialization method"""
        self.create_directory_structure()
        self.initialize_git()
        
        components = [comp['name'] for comp in project_config.get('components', [])]
        
        # Create components
        for component in components:
            self.create_component(component)
            
        # Create workflow files
        self.create_workflow_files(components)
        
        print(f"Project initialized successfully at {self.project_root}")

def main():
    parser = argparse.ArgumentParser(description='Initialize project structure')
    parser.add_argument('project_root', help='Path to project root directory')
    parser.add_argument('config', help='Path to project config YAML file')
    
    args = parser.parse_args()
    
    # Load project config
    with open(args.config, 'r') as f:
        project_config = yaml.safe_load(f)
        
    initializer = ProjectInitializer(args.project_root)
    initializer.initialize_project(project_config)

if __name__ == '__main__':
    main()
