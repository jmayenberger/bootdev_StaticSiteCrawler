# Static Site Generator

A static site generator project built in Python and deployed using [GitHub Pages](https://pages.github.com/).

## Overview

This project converts Markdown files into static HTML pages, stitches them together with CSS templates, and copies over supporting assets to produce a production-ready website. Cave: It does not support full markdown syntax.

## Directory Structure

- `content/`: Place all your **Markdown files** here. These are the source files that will be converted into HTML. 
    - Example: `content/index.md`, `content/blog/my-post.md`
- `.templates.html`: Place your HTML **template file** here. This dictates the layout and styling of the generated pages.
    - Your title will be placed at placeholder `{{ Title }}`
    - Your content will be placed at placeholder `{{ Content }}`
- `static/`: Place all your static assets here, such as **CSS files** and **images**
    - Example: `static/index.css`, `static/logo.png`
- `docs/`: The output directory for the generated site. This will be automatically created by the generator. **Do not edit this directory by hand.**

## Features

- Converts Markdown files to HTML pages.
- Supports user-defined CSS and templates.
- Copies static assets (css, images) into the output directory.
- Configurable `basepath` for correct routing with GitHub Pages.
- Simple CLI usage via `build.sh`.

## Getting Started

### Prerequisites

- Python 3.x
- [Git](https://git-scm.com/)
- (Optional) [Boot.dev CLI](https://github.com/bootdotdev/bootdev) for local testing

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jmayenberger/bootdev_StaticSiteCrawler
    cd bootdev_StaticSiteCrawler
    ```

### Building the Site

For local development:

```bash
python3 src/main.py
```
This generates the site from the contents of `content/`  and `static/`, outputting to the `docs/` directory, using the default `/` basepath.

For production (GitHub Pages):

```bash
./build.sh
```
This will generate your site with the correct basepath for GitHub Pages and output it to the `docs/` directory.

### Deployment

Your site is automatically deployed by GitHub Pages from the `docs/` directory on the `main` branch.  
After pushing updates, you can view your live site at:

```
https://YOUR_USERNAME.github.io/REPO_NAME/
```

## Configuration

Change the base path for deployment by passing it as a command-line argument:

```bash
python3 src/main.py "/BASEPATH/"
```


## License

MIT License

---

Built as part of [Boot.dev](https://boot.dev) coursework.
