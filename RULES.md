

## Branching Strategy:
Use a branching model, such as GitFlow or GitHub Flow, to manage code changes effectively.
Create feature branches for new features or bug fixes and merge them into the test branch after code review and testing.

## Commit Guidelines:
Write clear and descriptive commit messages.
Keep commits focused and atomic, addressing a single change or feature.
Use imperative language and present tense in commit messages (e.g., "Fix bug" instead of "Fixed bug").

## Code Reviews:
Require code reviews for all changes before merging into the test branch.
Define code review criteria, such as code style, best practices, and adherence to project guidelines.
Encourage constructive feedback and discussions during code reviews.

## Pull Requests:
DO NOT WORK IN THE MAIN BRANCH, PRODUCTION BRANCH AND TEST BRANCH, ALSO DO NOT DIRECTLY PUSH TO THOS BRANCHES. THESE ARE FOR CI/CD WORKFLOW.
WORK IN THE development branch or create your own feature branch, push commits to that branch
ALWAYS CREATE A PULL REQUEST TO THE TEST BRANCH AND WAIT FOR IT TO BE MERGED BY THE BRANCH MASTER AFTER THE CODE IS FULLY REVIEWED

## Coding Style:
Establish a clear and consistent coding style guide or stick to the used coding style guide.

## Testing:
Write unit tests and integration tests for critical functionality.
Ensure that all tests pass before merging code into the main branch.
Aim for high test coverage to maintain code reliability.

## Documentation:
Encourage comprehensive and up-to-date documentation for code, APIs, and project setup.
Include README files with instructions for installation, usage, and contribution guidelines.
Document any project-specific conventions or configurations.

## Version Control:
Avoid committing directly to the main branch.
Regularly pull changes from the main branch to keep your local branch up to date.
Use descriptive and meaningful branch names.
