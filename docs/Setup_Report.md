# Report: Setting Up Projects in VSCode with Multiple ClineAI Agents

This report outlines the process of organizing projects in VSCode to work effectively with multiple ClineAI agents, ensuring that each AI task remains manageable and within token limits.

---

## 1. Overview

To efficiently manage complex projects involving multiple AI tasks, we propose a structured approach that:

- Establishes a top-level workflow that integrates all sub-workflows.
- Separates the codebase into individual VSCode projects within `/src/libs`, with each subfolder representing a class or feature.
- Utilizes `task_classname.yaml` and `project_tasks.yaml` files to keep AI tasks organized and within the 40K token limit.
- Employs a `cline_init` script to automate the creation and updating of the project structure based on a `project.yaml` configuration file.

---

## 2. Project Structure

The project directory will be organized as follows:

```
/project_root/
├── project.yaml
├── project_tasks.yaml
├── src/
│   ├── main_project_files...
│   ├── libs/
│   │   ├── ClassName1/
│   │   │   ├── ClassName1.code-workspace
│   │   │   ├── task_ClassName1.yaml
│   │   │   ├── code_files...
│   │   │   └── ai_chatlogs/
│   │   ├── ClassName2/
│   │   │   ├── ClassName2.code-workspace
│   │   │   ├── task_ClassName2.yaml
│   │   │   ├── code_files...
│   │   │   └── ai_chatlogs/
│   │   └── ...
│   └── workflows/
│       ├── main_workflow.yaml
│       └── sub_workflows/
│           ├── workflow_ClassName1.yaml
│           ├── workflow_ClassName2.yaml
│           └── ...
```

- **`project.yaml`**: Contains overall project configuration.
- **`project_tasks.yaml`**: Tracks AI tasks across the project.
- **`/src/libs/`**: Contains subfolders for each class or feature.
- **`ClassNameX/`**: Individual VSCode project for a class.
  - **`ClassNameX.code-workspace`**: VSCode workspace file.
  - **`task_ClassNameX.yaml`**: AI task definition for the class.
  - **`ai_chatlogs/`**: Directory to store AI chat logs.
  - **`code_files...`**: Source code files for the class.
- **`/src/workflows/`**: Contains the main workflow and sub-workflow definitions.
  - **`main_workflow.yaml`**: Defines the top-level workflow integrating all sub-workflows.
  - **`sub_workflows/`**: Contains individual workflow definitions for each class.

---

## 3. The `cline_init` Script

The `cline_init` script automates project setup and updates based on `project.yaml`, managing both the top-level workflow and sub-workflows.

**Key Functions:**

- Reads `project.yaml` for project settings, class definitions, and workflow configurations.
- Creates or updates the `/src/libs/` directory structure.
- Generates individual VSCode projects for each class in `/src/libs/`.
- Generates workflow files in `/src/workflows/`, including `main_workflow.yaml` and sub-workflow files.
- Creates `task_ClassNameX.yaml` files for AI task management.
- Ensures each class subfolder is self-contained with its own AI chat logs and code files.
- Manages the integration of sub-workflows into the main workflow.

**Script Workflow:**

1. **Initialization**:
   - Run the script in the project root directory.
   - Parse `project.yaml` for classes, features, and workflow definitions.

2. **Subfolder Creation**:
   - For each class, create a subfolder in `/src/libs/` named after the class.
   - Initialize a new VSCode workspace within the class subfolder.

3. **Workflow Generation**:
   - Create `main_workflow.yaml` in `/src/workflows/`.
   - For each class, create a `workflow_ClassNameX.yaml` in `/src/workflows/sub_workflows/`.
   - Update `main_workflow.yaml` to include references to all sub-workflows.

4. **File Generation**:
   - Create `task_ClassNameX.yaml` for each class.
   - Set up an `ai_chatlogs/` directory to store AI interactions.

5. **Updating Existing Projects**:
   - The script detects new classes or workflows added to `project.yaml` and updates the project structure accordingly.
   - It updates existing directories without overwriting code files or chat logs.

---

## 4. Top-Level Workflow Management

- **Main Workflow (`main_workflow.yaml`)**:
  - Acts as the orchestrator for all sub-workflows.
  - Defines the order and dependencies between sub-workflows.
  - Ensures cohesive integration of all project components.

- **Sub-Workflows (`workflow_ClassNameX.yaml`)**:
  - Define the specific tasks and processes for each class.
  - Allow for isolated development and testing of individual features.
  - Facilitate reusability and modularity.

- **Script Responsibilities**:
  - The `cline_init` script updates `main_workflow.yaml` whenever new sub-workflows are added.
  - Manages the inclusion and sequence of sub-workflows in the main workflow.
  - Ensures consistency across workflow definitions.

---

## 5. Managing AI Tasks

- **Token Limit Considerations**:
  - Keeping AI tasks below 40K tokens ensures efficient processing.
  - By separating tasks into individual `task_ClassNameX.yaml` files, each AI agent works within manageable limits.

- **Chat Logs**:
  - Storing AI chat logs in each class's `ai_chatlogs/` directory keeps interactions organized and easily accessible.

- **Project-wide Task Tracking**:
  - `project_tasks.yaml` provides an overview of all AI tasks.
  - Workflows reference these tasks to maintain alignment between code and AI processes.

---

## 6. Development Workflow

**Adding a New Feature or Class:**

1. Update `project.yaml` with the new class and workflow definitions.
2. Run `cline_init` to generate the new class subfolder and workflow files.
3. Develop the feature within its dedicated subfolder.
4. Update `workflow_ClassNameX.yaml` with specific tasks for the feature.
5. The `cline_init` script updates `main_workflow.yaml` to include the new sub-workflow.
6. Integration with the main project occurs in `/src/`, where code from all classes is collected.

**Benefits:**

- **Modularity**: Encapsulates features, making code maintenance and updates more manageable.
- **Centralized Workflow Management**: The main workflow provides a clear overview of the project's execution flow.
- **Parallel Development**: Multiple developers or AI agents can work on different classes and workflows simultaneously without conflicts.
- **Scalability**: Easily accommodates new features by updating `project.yaml` and rerunning `cline_init`.

---

## 7. Conclusion

Implementing this structured approach in VSCode with the assistance of a `cline_init` script streamlines the development process when working with multiple ClineAI agents. It:

- Promotes organized code management with a clear hierarchy.
- Ensures AI tasks and workflows remain within optimal token limits.
- Facilitates easy addition of new features and their integration into the main workflow.
- Enhances collaboration and productivity through modularity and centralized workflow management.

This setup is particularly beneficial for complex projects where modularity, efficient AI task handling, and cohesive workflows are crucial.

---

## 8. Next Steps

- Develop the `cline_init` script based on the outlined functionality.
- Set up the initial `project.yaml`, `main_workflow.yaml`, and `project_tasks.yaml` files.
- Begin organizing existing code and workflows into the new structure.
- Test the integration of sub-workflows within the main workflow.
