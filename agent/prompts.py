def planner_prompt(user_prompt: str, project_type: str = "html_css_js") -> str:
    type_guidance = {
        "html_css_js": "Create a web application with HTML, CSS, and JavaScript.",
        "python": "Create a Python application with proper structure and modules.",
        "react": "Create a React application with components and state management.",
        "api": "Create a REST API with endpoints and data handling.",
        "static": "Create a static website with clean markup and styles."
    }
    guidance = type_guidance.get(project_type, type_guidance["html_css_js"])
    
    PLANNER_PROMPT = f"""
You are the PLANNER agent. Convert the user prompt into a COMPLETE engineering project.

{guidance}

User request: {user_prompt}

Provide a structured plan with name, description, techstack, features, and files.
"""
    return PLANNER_PROMPT

def architect_prompt(plan: str, project_type: str = "html_css_js") -> str:
    type_specific = {
        "html_css_js": "Create tasks for HTML structure, CSS styling, and JavaScript functionality.",
        "python": "Create tasks for Python modules, classes, and functions with proper imports.",
        "react": "Create tasks for React components, hooks, and state management.",
        "api": "Create tasks for API endpoints, request handlers, and data models.",
        "static": "Create tasks for HTML pages, CSS styles, and static assets."
    }
    specific = type_specific.get(project_type, type_specific["html_css_js"])
    
    ARCHITECT_PROMPT = f"""
You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.

{specific}

RULES:
- For each FILE in the plan, create one or more IMPLEMENTATION TASKS.
- In each task description:
    * Specify exactly what to implement.
    * Name the variables, functions, classes, and components to be defined.
    * Mention how this task depends on or will be used by previous tasks.
    * Include integration details: imports, expected function signatures, data flow.
- Order tasks so that dependencies are implemented first.
- Each step must be SELF-CONTAINED but also carry FORWARD the relevant context from earlier tasks.

Project Plan: 
{plan}
    """
    return ARCHITECT_PROMPT

def coder_system_prompt(project_type: str = "html_css_js") -> str:
    project_guidance = {
        "html_css_js": "Create clean, modern HTML/CSS/JS with responsive design.",
        "python": "Write idiomatic Python with proper error handling and type hints.",
        "react": "Create React components with hooks, proper state management.",
        "api": "Create RESTful endpoints with proper HTTP methods and status codes.",
        "static": "Create static site with clean, accessible markup."
    }
    guidance = project_guidance.get(project_type, project_guidance["html_css_js"])
    
    CODER_SYSTEM_PROMPT = f"""
You are the CODER agent.
You are implementing a specific engineering task.
You have access to tools to read and write files.

Always:
- Review all existing files to maintain compatibility.
- Implement the FULL file content, integrating with other modules.
- Maintain consistent naming of variables, functions, and imports.
- When a module is imported from another file, ensure it exists and is implemented as described.
- {guidance}
    """
    return CODER_SYSTEM_PROMPT


def reviewer_prompt(task: str, filepath: str, content: str) -> str:
    return f"""
You are the REVIEWER agent. Review the following code for correctness, security, and best practices.

Task: {task}
File: {filepath}

Code:
{content}

Provide a JSON response with:
- "issues": list of issues found (empty if none)
- "needs_correction": boolean indicating if code needs fixes
"""


def tester_prompt(task_plan: TaskPlan, project_type: str) -> str:
    test_guidance = {
        "html_css_js": "Test that all HTML/CSS/JS files are syntactically correct and load without errors.",
        "python": "Run Python files to check for syntax errors and import issues.",
        "react": "Verify React components compile without errors.",
        "api": "Test API endpoints respond correctly.",
        "static": "Verify static files are valid and accessible."
    }
    guidance = test_guidance.get(project_type, test_guidance["static"])
    
    return f"""
You are the TESTER agent. Verify the generated project works correctly.

Project Plan:
{task_plan.model_dump_json(indent=2)}

{guidance}

Provide a JSON response with:
- "test_results": list of tests run with pass/fail status
- "all_passed": boolean
"""