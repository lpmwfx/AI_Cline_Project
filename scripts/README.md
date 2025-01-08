# Project Converter Script

This script converts a project description markdown file into a structured project_tasks.yaml file.

## Requirements

- Python 3.6+
- PyYAML package (`pip install pyyaml`)

## Usage

```bash
# Basic usage (output will be input_file_name.yaml)
python project_converter.py path/to/project.md

# Specify output file
python project_converter.py path/to/project.md -o path/to/output.yaml
```

## Validation Checks

The script performs several validation checks:

1. Required Sections:
   - Overview
   - Features/Components
   - Requirements
   - Technical Specifications
   - Dependencies
   - Implementation Details

2. Structure Validation:
   - Ensures all required sections are present and not empty
   - Validates feature format in Features/Components section
   - Checks for proper markdown heading structure
   - Verifies project name and version format

3. Token Limits:
   - Enforces 40K token limit per task
   - Provides token estimation for tasks
   - Warns about tasks approaching token limits

4. Feature Format:
   - Validates feature naming convention
   - Checks sub-feature structure
   - Ensures proper task ID generation
   - Validates component references

## Output Structure

The script generates a YAML file with:

1. Project Information:
   - Name
   - Description
   - Version

2. Tasks:
   - High-level tasks for each feature
   - Sub-tasks with IDs and descriptions
   - Token estimations
   - Dependencies
   - Status tracking

3. Settings:
   - Maximum tokens per task
   - Allowed status values
   - Default status

4. Task Files:
   - References to individual component task files
   - Task ID mappings

## Error Handling

The script provides clear error messages for:
- Missing required sections
- Invalid structure
- File read/write errors
- Token limit violations
- Invalid feature formats

## Example

Using the template from `/project/project_template.md`:

```bash
python project_converter.py ../project/project_template.md
```

This will generate a properly structured project_tasks.yaml file based on the template content.

## Integration

This script is part of the project setup workflow and can be used:
1. During initial project setup
2. When updating project structure
3. For validating project documentation
4. To generate task files for new features

## Notes

- The script uses a simple token estimation (4 characters per token)
- Default token limit is set to 40,000 per task
- Empty sections are treated as errors
- Feature names are converted to component names by removing spaces
