from pydantic import BaseModel,Field,ConfigDict
from typing import Optional, List
from enum import Enum
class File(BaseModel):
    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(
        description="The purpose of the file, e.g. 'main application logic', 'data processing module', etc.")


class Plan(BaseModel):
    name: str = Field(
        description="The name of app to be built"
    )
    description: str = Field(
        description="A oneline description of the app to be built, e.g. 'A web application for managing personal finances'"
    )
    techstack: str = Field(
        description="The tech stack to be used for the app, e.g. 'python', 'javascript', 'react', 'flask', etc."
    )
    features: list[str] = Field(
        description="A list of features that the app should have, e.g. 'user authentication', 'data visualization', etc."
    )
    files: list[File] = Field(
        description="A list of files to be created, each with a 'path' and 'purpose'"
    )


class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(description="A detailed description of the task to be performed on the file, e.g. 'add user authentication', 'implement data processing logic', etc.")

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow") #allows to customize and control behaviour of BaseModel validation, serialization and structure.

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")
    retry_count: int = Field(0, description="Number of retries for current step")
    max_retries: int = Field(3, description="Maximum retries per step")


class ReviewState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task being reviewed")
    current_step_idx: int = Field(0, description="The index of the step being reviewed")
    issues: list[str] = Field(default_factory=list, description="Issues found during review")
    needs_correction: bool = Field(False, description="Whether code needs correction")


class TestState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task being tested")
    test_results: list[dict] = Field(default_factory=list, description="Results of tests run")
    all_passed: bool = Field(True, description="Whether all tests passed")


class ProjectType(str, Enum):
    HTML_CSS_JS = "html_css_js"
    PYTHON = "python"
    REACT = "react"
    API = "api"
    STATIC = "static"


class ReviewResult(BaseModel):
    issues: List[str] = Field(default_factory=list, description="List of issues found")
    needs_correction: bool = Field(False, description="Whether code needs correction")
    STATIC = "static"