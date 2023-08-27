#!/bin/bash

default_branch="main"  # Change this to your desired default branch
github_token="$GH_TOKEN"  # Change this to the name of the secret containing your Personal Access Token

# Check if the user provided the directory and commit message as arguments
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <directory_path> [<branch_name>] <commit_message>"
  exit 1
fi

directory_path="$1"

if [ "$#" -eq 2 ]; then
  branch_name="$default_branch"
  commit_message="$2"
else
  branch_name="$2"
  commit_message="$3"
fi

# Function to check if there are any changes to commit
check_changes() {
  if [ -z "$(git -C "$directory_path" status --porcelain)" ]; then
    echo "No changes to commit."
    exit 0
  fi
}

# Function to add changes, commit and push
commit_and_push() {
  git -C "$directory_path" add .
  git -C "$directory_path" commit -m "$commit_message"
  git -C "$directory_path" push "https://${github_token}@github.com/$GITHUB_REPOSITORY.git" "$branch_name"
}

# Main script logic
echo "Executing script to automate Git actions..."

# Ensure the provided directory is a Git repository
if ! git -C "$directory_path" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: Provided directory is not a Git repository."
  exit 1
fi

# Switch to the specified branch
git -C "$directory_path" checkout "$branch_name"

# Check for changes and proceed accordingly
check_changes

# Perform the commit and push
commit_and_push

echo "Changes committed and pushed successfully to the $branch_name branch in $directory_path."
