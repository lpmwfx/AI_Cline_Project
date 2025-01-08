# Project Tasks Organization: From Markdown to YAML

This document explains how to structure and generate the `project_tasks.yaml` file from an input project description markdown file.

## Input: Project Description Markdown

The input project description should be a markdown file that clearly outlines:

1. Project Overview
2. Features/Components
3. Requirements
4. Technical Specifications
5. Dependencies
6. Implementation Details

Example structure of input markdown:
```markdown
# Project Name

## Overview
Brief description of the project's purpose and goals.

## Features/Components
- Feature 1
  - Sub-feature 1.1
  - Sub-feature 1.2
- Feature 2
  - Sub-feature 2.1
  - Sub-feature 2.2

## Requirements
- Requirement 1
- Requirement 2

## Technical Specifications
- Language: Python 3.8+
- Framework: FastAPI
- Database: PostgreSQL

## Dependencies
- dependency1==1.0.0
- dependency2>=2.0.0

## Implementation Details
Detailed explanation of implementation approach...
```

## Output: project_tasks.yaml Structure

The `project_tasks.yaml` file organizes tasks in a hierarchical structure that maps to the project components while ensuring each task stays within the 40K token limit.

```yaml
project:
  name: "Project Name"
  description: "Brief project description"
  version: "1.0.0"

tasks:
  # High-level tasks derived from Features/Components
  - id: "TASK-1"
    name: "Feature 1 Implementation"
    description: "Implementation of Feature 1"
    components:
      - "Feature1"
    sub_tasks:
      - id: "TASK-1.1"
        name: "Sub-feature 1.1"
        description: "Implementation of Sub-feature 1.1"
        estimated_tokens: 25000
        dependencies: []
        status: "pending"
        
      - id: "TASK-1.2"
        name: "Sub-feature 1.2"
        description: "Implementation of Sub-feature 1.2"
        estimated_tokens: 15000
        dependencies: ["TASK-1.1"]
        status: "pending"

  - id: "TASK-2"
    name: "Feature 2 Implementation"
    description: "Implementation of Feature 2"
    components:
      - "Feature2"
    sub_tasks:
      - id: "TASK-2.1"
        name: "Sub-feature 2.1"
        description: "Implementation of Sub-feature 2.1"
        estimated_tokens: 20000
        dependencies: []
        status: "pending"

      - id: "TASK-2.2"
        name: "Sub-feature 2.2"
        description: "Implementation of Sub-feature 2.2"
        estimated_tokens: 30000
        dependencies: ["TASK-2.1"]
        status: "pending"

# Global settings and constraints
settings:
  max_tokens_per_task: 40000
  default_status: "pending"
  allowed_statuses:
    - "pending"
    - "in_progress"
    - "completed"
    - "blocked"

# References to individual task files
task_files:
  - path: "src/libs/Feature1/task_Feature1.yaml"
    tasks: ["TASK-1.1", "TASK-1.2"]
  - path: "src/libs/Feature2/task_Feature2.yaml"
    tasks: ["TASK-2.1", "TASK-2.2"]
```

## Conversion Process

1. **Project Information Extraction**
   - Extract project name, description, and version from the markdown header and overview sections
   - Place these in the `project` section of the YAML

2. **Task Identification**
   - Analyze the Features/Components section
   - Create high-level tasks for each main feature
   - Break down sub-features into sub-tasks
   - Ensure each task has a unique ID

3. **Token Estimation**
   - Analyze the complexity and scope of each task
   - Estimate token count based on:
     - Code complexity
     - Documentation requirements
     - Test coverage needs
   - Ensure no task exceeds the 40K token limit
   - Split tasks if necessary to stay within limits

4. **Dependency Mapping**
   - Identify dependencies between tasks
   - Map these in the YAML structure
   - Ensure circular dependencies are avoided

5. **Component Organization**
   - Create task files for each component
   - Reference these files in the main project_tasks.yaml
   - Map tasks to their respective components

## Task File Organization

Each component gets its own task file (`task_classname.yaml`) that contains detailed information about its specific tasks. These files are referenced in the main `project_tasks.yaml`.

Example `task_Feature1.yaml`:
```yaml
component: "Feature1"
tasks:
  - id: "TASK-1.1"
    name: "Sub-feature 1.1"
    description: "Detailed description of sub-feature 1.1 implementation"
    steps:
      - "Step 1: Initialize component"
      - "Step 2: Implement core functionality"
      - "Step 3: Add error handling"
    acceptance_criteria:
      - "Criterion 1"
      - "Criterion 2"
    estimated_tokens: 25000
    status: "pending"

  - id: "TASK-1.2"
    name: "Sub-feature 1.2"
    description: "Detailed description of sub-feature 1.2 implementation"
    steps:
      - "Step 1: Design interface"
      - "Step 2: Implement logic"
    acceptance_criteria:
      - "Criterion 1"
      - "Criterion 2"
    estimated_tokens: 15000
    dependencies: ["TASK-1.1"]
    status: "pending"
```

## Benefits of This Structure

1. **Token Management**
   - Clear visibility of token usage per task
   - Easy identification of tasks approaching token limits
   - Ability to split tasks when needed

2. **Dependency Tracking**
   - Clear visualization of task dependencies
   - Helps in planning task execution order
   - Prevents circular dependencies

3. **Progress Monitoring**
   - Status tracking for each task
   - Clear view of blocked tasks
   - Easy progress reporting

4. **Modularity**
   - Tasks organized by component
   - Individual task files for detailed information
   - Easy to maintain and update

5. **Integration with Workflows**
   - Tasks can be referenced in workflow files
   - Supports automation of task execution
   - Facilitates CI/CD integration

## Usage in Development

1. **Initial Setup**
   - Create project description markdown
   - Run conversion process
   - Generate project_tasks.yaml and component task files

2. **Development Process**
   - Reference task files for implementation details
   - Update task status as work progresses
   - Track token usage during development

3. **Maintenance**
   - Update task files as requirements change
   - Add new tasks as needed
   - Archive completed tasks

4. **Integration**
   - Use task IDs in commit messages
   - Reference tasks in documentation
   - Link tasks to test cases
