# Static Site Generator
Static Site Generator is a Python application that converts Markdown documents into static HTML pages. The project began as a guided Boot.dev exercise before being extended with comprehensive automated testing and refactoring.

## Technical Highlights
- Object-oriented HTML node architecture
- Markdown parsing and transformation pipeline
- Recursive HTML rendering
- File-system-based build pipeline
- Automated testing with edge-case coverage
- Separation of parsing and rendering concerns

## Tech Stack
- Python
- unittest

## Live Demo
Demonstration of the static site:

https://ajrollerson.github.io/staticsitegenerator/

## Quick Start
The following commands assume a Bash/WSL environment.
### Clone the Repository
```bash
git clone https://github.com/ajrollerson/staticsitegenerator.git
cd staticsitegenerator
```

### Build the Site
```bash
python3 src/main.py
```
Generates the static site in the `docs/` directory using root-relative paths.

### Build for GitHub Pages
```bash
python3 src/main.py "/staticsitegenerator/"
```

Generates the site using `/staticsitegenerator/` as the root path, which is required because GitHub Pages serves the project from a repository subdirectory.

### Run Tests
```bash
./test.sh
```

## Key Features
### Core Functionality
- Convert Markdown documents into HTML
- Parse block-level Markdown elements
- Parse inline Markdown elements
- Render HTML through recursive node structures
- Generate static HTML files from source documents

### Independent Extensions
- Expanded the automated test suite to 78 tests
- Added edge-case coverage for Markdown parsing behaviour
- Added tests supporting future parser extensions
- Refactored parsing logic to improve code organisation

## Design Choices
### Comprehensive Test Coverage
The original project provided limited automated test coverage, so the test suite was expanded to cover parser behaviour and edge cases. This provides greater confidence in the existing implementation while creating a safety net for future changes to the parsing pipeline.

### Functional Parsing Logic
Parts of `block_to_html.py` were implemented using a more functional style to reduce repetition and keep individual transformations concise. While this approach can make some operations more compact, it also increases cognitive load when compared with a more explicit implementation. This trade-off highlighted the importance of balancing brevity against maintainability when structuring parsing logic.

## Known Limitations
- This parser supports a subset of Markdown and does not yet handle recursive inline Markdown elements

## Future Improvements
- Add support for recursive inline Markdown
- Continue expanding test coverage as the parser develops

