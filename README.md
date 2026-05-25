Readme – Static Site Generator

This static site generator was built as part of a guided Boot.dev project and extended with a comprehensive test suite and additional engineering improvements.

Live demo: https://ajrollerson.github.io/staticsitegenerator/

Key skills and knowledge developed: 
•	Object-oriented design using node-based structures
•	File system manipulation and build pipeline design 
•	Unit testing with edge-case coverage 
•	Markdown parsing and transformation pipelines

Key features:

The base project implemented the following:
•	Markdown-to-HTML conversion system 
•	Recursive HTML node rendering engine 
•	File-based build and output generation system

Personal additions:
•	Expanded test suite to 78 tests covering edge cases and parser behaviour

Installation & Usage

•	Clone the repository:

git clone https://github.com/ajrollerson/staticsitegenerator

cd staticsitegenerator

• Local preview

python3 src/main.py 

Builds the site for local preview using root-relative paths.

• GitHub Pages build

python3 src/main.py "/staticsitegenerator/" 

Required when building for GitHub Pages, which serves the site from a subdirectory.


Design choices:

•	A comprehensive test suite was implemented to validate expected behaviour and edge cases, and to support future extension of the parser. In the future, such tests will help support further extensions and guard against unexpected bugs that emerge.

• Regarding block_to_html.py, a more functional style was adopted in parts of the codebase for brevity. However, this increases cognitive overhead when tracing execution flow and may reduce long-term maintainability.

Known limitations:

•	This parser supports a subset of Markdown and does not yet handle recursive inline markdown elements.

Future improvements:
•	Will include features to parse recursive inline markdown
•	Will continue updating the extensive test suite as the project expands.

