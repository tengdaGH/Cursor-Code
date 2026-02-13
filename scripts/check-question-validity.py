#!/usr/bin/env python3
"""
Check validity of all questions in the JSON file.
Reports issues with question fields, posts, etc.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
JSON_FILE = PROJECT_ROOT / "data" / "writing-academic-discussion-prompts.json"

def check_question_validity(q, suggest_fixes=False):
    """Check if a question has valid content. Returns list of issues and optional fixes."""
    issues = []
    fixes = []
    q_id = q.get("id", "UNKNOWN")
    
    # Check question field
    question = q.get("question", "").strip()
    if not question:
        issues.append({
            "type": "missing_question",
            "severity": "error",
            "message": f"{q_id}: Missing question field",
            "suggestion": "Add a complete professor question starting with 'Your professor is teaching...'"
        })
    elif len(question) < 20:
        issues.append({
            "type": "question_too_short",
            "severity": "error",
            "message": f"{q_id}: Question too short ({len(question)} chars): '{question[:50]}...'",
            "suggestion": f"Question should be at least 50 characters. Current: {len(question)} chars"
        })
    elif question[0].islower() and len(question) < 50:
        # Might be a fragment
        issues.append({
            "type": "question_fragment",
            "severity": "error",
            "message": f"{q_id}: Question looks like fragment (starts lowercase): '{question[:50]}...'",
            "suggestion": "Question should start with 'Your professor is teaching...' and be a complete sentence"
        })
    elif question.endswith(("?", ":", ".", ",")) and len(question) < 50:
        # Might be incomplete
        if not any(word in question.lower() for word in ["do you", "should", "what", "why", "how", "which"]):
            issues.append({
                "type": "question_incomplete",
                "severity": "warning",
                "message": f"{q_id}: Question might be incomplete: '{question[:50]}...'",
                "suggestion": "Ensure question is complete and includes context (e.g., 'Your professor is teaching...')"
            })
    
    # Check posts
    posts = q.get("posts", [])
    if len(posts) < 2:
        issues.append({
            "type": "insufficient_posts",
            "severity": "error",
            "message": f"{q_id}: Less than 2 posts",
            "suggestion": "Add at least 2 student posts"
        })
    else:
        for i, post in enumerate(posts, 1):
            text = post.get("text", "").strip()
            author = post.get("author", "")
            
            if not text:
                issues.append({
                    "type": "empty_post",
                    "severity": "error",
                    "message": f"{q_id}: Post {i} ({author}) has no text",
                    "suggestion": f"Add content to post {i}"
                })
            elif len(text) < 10:
                issues.append({
                    "type": "post_too_short",
                    "severity": "error",
                    "message": f"{q_id}: Post {i} ({author}) too short: '{text}'",
                    "suggestion": f"Post should be at least 20 characters. Current: {len(text)} chars"
                })
            elif "###" in text or "**Category:**" in text or "**Professor Question:**" in text:
                issues.append({
                    "type": "markdown_in_post",
                    "severity": "error",
                    "message": f"{q_id}: Post {i} ({author}) contains markdown headers (parsing error)",
                    "suggestion": "Remove markdown headers from post text. This indicates a parsing error."
                })
            elif text.startswith("professor is teaching") and len(text) < 50:
                issues.append({
                    "type": "incomplete_extraction",
                    "severity": "error",
                    "message": f"{q_id}: Post {i} ({author}) looks like incomplete extraction: '{text[:50]}...'",
                    "suggestion": "Post appears to contain question text instead of student response. Fix in Markdown source."
                })
            elif "In your response. you should do the following." in text:
                # This is instruction text, not student post
                if len(text) < 100:
                    issues.append({
                        "type": "instruction_text",
                        "severity": "error",
                        "message": f"{q_id}: Post {i} ({author}) contains instruction text instead of student post",
                        "suggestion": "Remove instruction text from post. Add actual student response."
                    })
    
    return issues

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check validity of academic discussion questions")
    parser.add_argument("--suggest", "-s", action="store_true", help="Show fix suggestions")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if not JSON_FILE.exists():
        print(f"Error: JSON file not found: {JSON_FILE}")
        sys.exit(1)
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    prompts = data.get("prompts", [])
    print(f"Checking {len(prompts)} questions...\n")
    
    all_issues = []
    issue_by_type = {}
    issue_by_severity = {"error": 0, "warning": 0}
    
    for prompt in prompts:
        issues = check_question_validity(prompt, suggest_fixes=args.suggest)
        if issues:
            all_issues.extend(issues)
            for issue in issues:
                issue_type = issue.get("type", "unknown")
                severity = issue.get("severity", "unknown")
                issue_by_type[issue_type] = issue_by_type.get(issue_type, 0) + 1
                if severity in issue_by_severity:
                    issue_by_severity[severity] += 1
    
    if all_issues:
        if args.json:
            # Output as JSON
            output = {
                "total_issues": len(all_issues),
                "questions_checked": len(prompts),
                "issues_by_type": issue_by_type,
                "issues_by_severity": issue_by_severity,
                "issues": all_issues
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            # Human-readable output
            print(f"Found {len(all_issues)} issues:\n")
            
            # Group by severity
            errors = [i for i in all_issues if i.get("severity") == "error"]
            warnings = [i for i in all_issues if i.get("severity") == "warning"]
            
            if errors:
                print("❌ ERRORS:")
                for issue in errors:
                    print(f"  • {issue['message']}")
                    if args.suggest and "suggestion" in issue:
                        print(f"    💡 {issue['suggestion']}")
                print()
            
            if warnings:
                print("⚠️  WARNINGS:")
                for issue in warnings:
                    print(f"  • {issue['message']}")
                    if args.suggest and "suggestion" in issue:
                        print(f"    💡 {issue['suggestion']}")
                print()
            
            # Count by question ID
            question_ids = set()
            for issue in all_issues:
                q_id = issue["message"].split(":")[0]
                question_ids.add(q_id)
            
            print(f"📊 Summary:")
            print(f"   Total issues: {len(all_issues)}")
            print(f"   Errors: {issue_by_severity.get('error', 0)}")
            print(f"   Warnings: {issue_by_severity.get('warning', 0)}")
            print(f"   Questions with issues: {len(question_ids)}")
            print(f"   Questions OK: {len(prompts) - len(question_ids)}")
            
            if issue_by_type:
                print(f"\n📋 Issues by type:")
                for issue_type, count in sorted(issue_by_type.items()):
                    print(f"   - {issue_type}: {count}")
            
            print(f"\n📋 Questions with issues:")
            for q_id in sorted(question_ids, key=lambda x: int(x[1:]) if x[1:].isdigit() else 999):
                print(f"   - {q_id}")
        
        return 1
    else:
        print("✅ All questions are valid!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
