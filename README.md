# Static Site Generator

A static site generator built from scratch in Python. It converts a directory
of Markdown files into a fully rendered HTML website, using a single HTML
template and a CSS stylesheet.


> **Note:** This project was built for educational purposes as part of the
> [Boot.dev](https://www.boot.dev) backend developer path. It is not intended
> for production use — the goal was to understand how static site generators
> work by building one from scratch.

---

## Built With
- Python 3
- Standard libraries (`os`, `pathlib`, `shutil`, `re`, `sys`)
- No frameworks, no dependencies

---

## How It Works
1. The `docs/` directory is wiped clean on every run
2. Static assets (CSS, images) are copied from `static/` to `docs/`
3. Every `.md` file in `content/` is recursively discovered and converted to HTML
4. Each HTML page is rendered using `template.html` as the base layout, rewriting relative asset paths to support nested subdirectories (such as GitHub Pages subfolders)
5. The output mirrors the `content/` directory structure inside `docs/`

---

## Requirements

- Python 3.x
- No external dependencies — standard library only

---

## Usage

### Build and Serve (local)

```bash
./main.sh
```
This will:
* Generate all HTML pages into public/
* Start a local host server at http://localhost:8888


### Build GitHub Pages
To build the site with a configured subfolder path (useful for hosting on GitHub Pages):

```bash
./build.sh
```

This script runs the generator and passes your repository subdirectory as an argument so all internal links (`href` and `src`) are mapped correctly.


### Run Tests

```bash
./test.sh
```

---

## Markdown Features Supported
|Feature|Syntax|
|---|---|
|Heading|`# H1`, `## H2`, etc.|
|Bold|`**bold**`|
|Italic|`_italic_`|
|Inline code|`` `code` ``|
|Code blocks|` ``` `fencde blocks|
|Links|`[text](url)`|
|Images|`![alt](url)`|
|Blockquotes|`> quote`|
|Ordered lists|`1. item`|
|Unordered lists|`- item`|

---

## Template System
Pages are rendered by injecting content into `template.html` using two placeholder tokens:
* `{{ Title }}` — replaced with the first # H1 heading from the markdown file
* `{{ Content }}` — replaced with the full HTML-converted body

---

## Adding New Pages
1. Create a new folder inside content/
2. Add an index.md file with a # Title as the first heading
3. Run ./main.sh — the page will be automatically discovered and generated

Example:
```
content/
└── about/
    └── index.md   <-- becomes public/about/index.html
```

---

## Author
[tsuyoshi64](https://github.com/tsuyoshi64) - guided by [Boot.dev](https://www.boot.dev)

---

## License
[MIT](./LICENSE)
