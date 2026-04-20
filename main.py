import argparse
from agent.graph import agent

def main():
    parser = argparse.ArgumentParser(description="Shard - AI Software Engineer")
    parser.add_argument("prompt", type=str, help="Describe the app you want to build")
    parser.add_argument("--type", "-t", type=str, default="html_css_js",
                        choices=["html_css_js", "python", "react", "api", "static"],
                        help="Project type (default: html_css_js)")
    args = parser.parse_args()

    print(f"\n🚀 Building: {args.prompt}")
    print(f"📦 Project type: {args.type}\n")

    result = agent.invoke(
        {"user_prompt": args.prompt, "project_type": args.type},
        config={"recursion_limit": 100}
    )

    print("\n✅ Done! Check the 'generated_project' folder.\n")

if __name__ == "__main__":
    main()