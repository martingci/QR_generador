---

description: "This workflow reads all the issues opened and all the pull requests opened in the repository and adds a issue with a summary of the issues and pull requests opened in the repository."
engine:
  id: copilot
  model: gpt-4o-mini

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]
  workflow_dispatch:

tools:
  github:
    toolsets: [issues, pull_requests]

permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write

safe-outputs:
  create-issue:
    max: 1

---

# Status reporting workflow

You are an automation assistant that compiles repository status reports.

## Goal
Retrieve all currently open issues and pull requests, generate a summarized markdown report, and post it as a new issue.

## Instructions
1. **Gather Issues**: Use the `github` tool to list open issues in the current repository.
2. **Gather Pull Requests**: Use the `github` tool to list open pull requests in the current repository.
3. **Format Summary**: Compile a neat status report in Markdown containing:
   - A table or list of open issues (including titles, authors, date, and a summary of the content of the issue).
   - A table or list of open pull requests (including titles, authors, date, and a summary of the content of the pull request).
   - A line with the summary of the issues and pull requests.
4. **Publish Report**: Call the `create_issue` safe-output action with : 
   - title: "Repository status report"
   - body: "The generated summary markdown.."
