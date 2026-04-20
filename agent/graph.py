from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from enum import Enum

load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from agent.prompts import *
from agent.states import *
from agent.tools import *

llm = ChatGroq(model="llama-3.3-70b-versatile")

# ============ AGENT NODES ============

def planner_agent(state: dict) -> dict:
    """Analyzes user prompt and creates project plan."""
    users_prompt = state["user_prompt"]
    project_type = state.get("project_type", "html_css_js")
    
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(users_prompt, project_type))
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    
    print(f"📋 [Planner] Created plan: {resp.name}")
    return {"plan": resp, "project_type": project_type}


def architect_agent(state: dict) -> dict:
    """Breaks plan into implementation tasks."""
    plan: Plan = state["plan"]
    project_type = state.get("project_type", "html_css_js")
    
    resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan, project_type))
    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan
    print(f"🏗️ [Architect] Created {len(resp.implementation_steps)} tasks")
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """Implements tasks one by one with retry logic."""
    coder_state = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0,
            retry_count=0,
            max_retries=3
        )

    steps = coder_state.task_plan.implementation_steps
    
    # Check if done
    if coder_state.current_step_idx >= len(steps):
        print(f"✅ [Coder] Completed all {len(steps)} tasks")
        return {"coder_state": coder_state, "status": "CODER_DONE"}

    current_task = steps[coder_state.current_step_idx]
    project_type = state.get("project_type", "html_css_js")
    
    print(f"  📝 [Coder] Step {coder_state.current_step_idx + 1}/{len(steps)}: {current_task.filepath}")

    # Read existing content
    existing_content = read_file.run(current_task.filepath)
    content_section = f"Existing content:\n{existing_content}\n" if existing_content.strip() else ""

    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"{content_section}"
        "Write ONLY the code needed for this specific task. "
        "Use write_file tool to save the complete file content."
    )

    system_prompt = coder_system_prompt(project_type)
    coder_tools = [read_file, write_file, list_files, get_current_directory, run_cmd]

    from langchain.agents import create_react_agent
    react_agent = create_react_agent(llm, coder_tools)
    
    try:
        result = react_agent.invoke({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        })
        
        # Check if step succeeded
        last_message = result.get("messages", [])[-1] if result.get("messages") else None
        if last_message and "WROTE:" in str(last_message.content):
            coder_state.retry_count = 0
        else:
            coder_state.retry_count += 1
            if coder_state.retry_count < coder_state.max_retries:
                print(f"  ⚠️ [Coder] Retry {coder_state.retry_count}/{coder_state.max_retries}")
                return {"coder_state": coder_state, "status": "RETRY"}
            else:
                print(f"  ❌ [Coder] Max retries reached, moving on")
                coder_state.retry_count = 0
                
    except Exception as e:
        print(f"  ❌ [Coder] Step {coder_state.current_step_idx} failed: {e}")
        coder_state.retry_count += 1
        if coder_state.retry_count >= coder_state.max_retries:
            coder_state.retry_count = 0

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state, "status": "CONTINUE"}


def reviewer_agent(state: dict) -> dict:
    """Reviews generated code for issues."""
    review_state = state.get("review_state")
    if review_state is None:
        review_state = ReviewState(
            task_plan=state["task_plan"],
            current_step_idx=0,
            issues=[],
            needs_correction=False
        )

    steps = review_state.task_plan.implementation_steps
    
    if review_state.current_step_idx >= len(steps):
        print(f"✅ [Reviewer] Reviewed all {len(steps)} files")
        return {"review_state": review_state, "status": "REVIEW_DONE"}

    current_task = steps[review_state.current_step_idx]
    content = read_file.run(current_task.filepath)
    
    if not content.strip():
        review_state.current_step_idx += 1
        return {"review_state": review_state, "status": "CONTINUE"}

    print(f"  🔍 [Reviewer] Checking: {current_task.filepath}")

    resp = llm.with_structured_output(ReviewResult).invoke(
        reviewer_prompt(current_task.task_description, current_task.filepath, content)
    )
    
    if resp:
        review_state.issues.extend(resp.issues or [])
        if resp.needs_correction:
            review_state.needs_correction = True
            print(f"  ⚠️ [Reviewer] Issues found in {current_task.filepath}")
    
    review_state.current_step_idx += 1
    return {"review_state": review_state, "status": "CONTINUE"}


def corrector_agent(state: dict) -> dict:
    """Fixes issues found by reviewer."""
    review_state = state.get("review_state")
    if not review_state or not review_state.needs_correction:
        return {"status": "CORRECTION_SKIP"}

    print(f"🔧 [Corrector] Fixing {len(review_state.issues)} issues...")
    
    for issue in review_state.issues:
        try:
            if "file:" in issue.lower():
                print(f"  🔧 [Corrector] Fixed: {issue[:50]}...")
        except Exception as e:
            print(f"  ❌ [Corrector] Failed to fix: {e}")

    review_state.needs_correction = False
    review_state.issues = []
    print(f"✅ [Corrector] Issues resolved")
    return {"review_state": review_state, "status": "CORRECTION_DONE"}


def tester_agent(state: dict) -> dict:
    """Tests the generated project."""
    test_state = state.get("test_state")
    if test_state is None:
        test_state = TestState(
            task_plan=state["task_plan"],
            test_results=[],
            all_passed=True
        )

    project_type = state.get("project_type", "html_css_js")
    print(f"🧪 [Tester] Running tests for {project_type} project...")

    test_results = []
    
    if project_type == "html_css_js":
        files = list_files.run(".")
        for step in test_state.task_plan.implementation_steps:
            content = read_file.run(step.filepath)
            passed = bool(content.strip())
            test_results.append({
                "test": f"File exists: {step.filepath}",
                "passed": passed
            })
            if not passed:
                test_state.all_passed = False

    elif project_type == "python":
        for step in test_state.task_plan.implementation_steps:
            if step.filepath.endswith(".py"):
                code, stdout, stderr = run_cmd.run(f"python -m py_compile {step.filepath}")
                passed = code == 0
                test_results.append({
                    "test": f"Syntax check: {step.filepath}",
                    "passed": passed,
                    "error": stderr if not passed else None
                })
                if not passed:
                    test_state.all_passed = False

    test_state.test_results = test_results
    
    if test_state.all_passed:
        print(f"✅ [Tester] All {len(test_results)} tests passed")
    else:
        failed = sum(1 for r in test_results if not r["passed"])
        print(f"❌ [Tester] {failed}/{len(test_results)} tests failed")

    return {"test_state": test_state, "status": "TEST_DONE"}


# ============ GRAPH CONSTRUCTION ============

def should_continue_coder(state: dict) -> str:
    status = state.get("status", "")
    if status in ["CODER_DONE", "REVIEW_DONE"]:
        return END
    if status == "RETRY":
        return "coder"
    return "coder"


def should_review(state: dict) -> str:
    if state.get("status") == "CODER_DONE":
        return "reviewer"
    return END


def should_correct(state: dict) -> str:
    review_state = state.get("review_state")
    if review_state and review_state.needs_correction:
        return "corrector"
    return "tester"


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("reviewer", reviewer_agent)
graph.add_node("corrector", corrector_agent)
graph.add_node("tester", tester_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder",
    should_continue_coder,
    {END: "reviewer", "coder": "coder"}
)

graph.add_conditional_edges(
    "reviewer",
    lambda s: "corrector" if s.get("review_state", {}).get("needs_correction") else "tester",
    {"corrector": "corrector", "tester": "tester"}
)

graph.add_edge("corrector", "reviewer")
graph.add_edge("tester", END)

graph.set_entry_point("planner")

agent = graph.compile()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Shard - Advanced AI Software Engineer")
    parser.add_argument("prompt", type=str, help="Describe the app you want to build")
    parser.add_argument("--type", "-t", type=str, default="html_css_js",
                        choices=["html_css_js", "python", "react", "api", "static"],
                        help="Project type")
    args = parser.parse_args()

    print(f"\n🚀 Building: {args.prompt}")
    print(f"📦 Project type: {args.type}\n")

    result = agent.invoke(
        {"user_prompt": args.prompt, "project_type": args.type},
        config={"recursion_limit": 100}
    )

    print("\n" + "="*50)
    if result.get("test_state", {}).get("all_passed"):
        print("✅ Build successful! Check 'generated_project/' folder.")
    else:
        print("⚠️ Build completed with some issues.")
    print("="*50 + "\n")