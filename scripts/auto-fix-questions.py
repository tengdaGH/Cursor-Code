#!/usr/bin/env python3
"""
Auto-fix common issues in academic discussion questions.

This script detects and fixes common patterns of incomplete or malformed questions.
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"
JSON_FILE = PROJECT_ROOT / "data" / "writing-academic-discussion-prompts.json"


def detect_common_issues(md_content):
    """Detect common issues in Markdown content."""
    issues = []
    
    # Find all question blocks
    question_blocks = re.split(r'\n###\s+(D\d+)', md_content)
    
    for i in range(1, len(question_blocks), 2):
        if i + 1 >= len(question_blocks):
            break
        
        q_id = question_blocks[i]
        content = question_blocks[i + 1]
        
        # Check for incomplete question
        question_match = re.search(
            r'\*\*Professor Question:\*\*\s*\n(.*?)\n\*\*Student Posts:\*\*',
            content,
            re.DOTALL
        )
        
        if question_match:
            question = question_match.group(1).strip()
            
            # Issue: Question too short or starts with lowercase
            if len(question) < 30 or (question[0].islower() and len(question) < 50):
                issues.append({
                    "id": q_id,
                    "type": "incomplete_question",
                    "question": question,
                    "content": content
                })
            
            # Issue: Question looks like a fragment
            if question.endswith(("?", ":", ".", ",")) and len(question) < 50:
                if not question.startswith("Your professor"):
                    issues.append({
                        "id": q_id,
                        "type": "question_fragment",
                        "question": question,
                        "content": content
                    })
        
        # Check for incomplete posts
        post1_match = re.search(
            r'-\s+\*\*\[?Author1\]?:\*\*\s*\n?(.*?)(?=\n-\s+\*\*\[?Author2\]?:\*\*|\n\*\*Notes:\*\*|\n\*\*Status:\*\*|\n---|\Z)',
            content,
            re.DOTALL
        )
        
        if post1_match:
            post1 = post1_match.group(1).strip()
            if post1.startswith("professor is teaching") and len(post1) < 50:
                issues.append({
                    "id": q_id,
                    "type": "incomplete_post1",
                    "post": post1,
                    "content": content
                })
    
    return issues


def suggest_fix(issue):
    """Suggest a fix for an issue."""
    q_id = issue["id"]
    issue_type = issue["type"]
    
    suggestions = []
    
    if issue_type == "incomplete_question":
        question = issue["question"]
        # Try to infer from title or category
        title_match = re.search(r'-\s+(.+?)\s+\(', issue["content"])
        if title_match:
            title = title_match.group(1)
            # Extract topic from title
            topic = title.split(" - ")[-1] if " - " in title else title
            
            category_match = re.search(r'\*\*Category:\*\*\s*(.+?)\s*\n', issue["content"])
            category = category_match.group(1).strip() if category_match else "other"
            
            # Generate suggested question based on category and topic
            category_contexts = {
                "Education": "Your professor is teaching a class on education.",
                "Economy": "Your professor is teaching a class on economics.",
                "Environment": "Your professor is teaching a class on environmental science.",
                "Society": "Your professor is teaching a class on sociology.",
                "Technology": "Your professor is teaching a class on technology.",
                "Other": "Your professor is teaching a class."
            }
            
            context = category_contexts.get(category, category_contexts["Other"])
            
            # Check if question ends with a question mark or similar
            if question.endswith("?"):
                suggested = f"{context} {question}"
            elif "?" in question:
                suggested = f"{context} {question}"
            else:
                # Try to make it a question
                suggested = f"{context} What do you think about {topic.lower()}? Why?"
            
            suggestions.append({
                "type": "add_context",
                "original": question,
                "suggested": suggested,
                "reason": "Question appears incomplete. Adding professor context."
            })
    
    elif issue_type == "question_fragment":
        question = issue["question"]
        # Try to complete the question
        if question.endswith("?"):
            suggested = f"Your professor is teaching a class. {question}"
        else:
            suggested = f"Your professor is teaching a class. {question} Why?"
        
        suggestions.append({
            "type": "complete_question",
            "original": question,
            "suggested": suggested,
            "reason": "Question appears to be a fragment. Adding context."
        })
    
    elif issue_type == "incomplete_post1":
        post = issue["post"]
        suggestions.append({
            "type": "fix_post",
            "original": post,
            "suggested": "[Need to extract from image or reconstruct]",
            "reason": "Post contains question text instead of student response."
        })
    
    return suggestions


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto-detect and suggest fixes for question issues")
    parser.add_argument("--dry-run", action="store_true", help="Only show suggestions, don't apply fixes")
    parser.add_argument("--apply", action="store_true", help="Apply suggested fixes (use with caution)")
    args = parser.parse_args()
    
    if not BANK_FILE.exists():
        print(f"Error: Question bank file not found: {BANK_FILE}")
        sys.exit(1)
    
    # Read Markdown
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Detect issues
    print("Detecting common issues...")
    issues = detect_common_issues(md_content)
    
    if not issues:
        print("✅ No common issues detected!")
        return 0
    
    print(f"\nFound {len(issues)} potential issues:\n")
    
    # Group by type
    issues_by_type = {}
    for issue in issues:
        issue_type = issue["type"]
        if issue_type not in issues_by_type:
            issues_by_type[issue_type] = []
        issues_by_type[issue_type].append(issue)
    
    # Show issues and suggestions
    for issue_type, type_issues in issues_by_type.items():
        print(f"📋 {issue_type} ({len(type_issues)} issues):")
        for issue in type_issues:
            print(f"  • {issue['id']}")
            suggestions = suggest_fix(issue)
            if suggestions:
                for sug in suggestions:
                    print(f"    💡 {sug['reason']}")
                    print(f"       Original: {sug['original'][:60]}...")
                    print(f"       Suggested: {sug['suggested'][:60]}...")
        print()
    
    if args.dry_run:
        print("🔍 Dry run mode - no changes made")
        print("Use --apply to apply fixes (not implemented yet)")
    elif args.apply:
        print("⚠️  Auto-fix not fully implemented yet.")
        print("Please manually fix issues in the Markdown file based on suggestions above.")
    
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
