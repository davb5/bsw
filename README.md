# bsw
Build Static Website - a simple static website generator


## Usage (the short version)

```
usage: bsw.py [-h] [-C] [-s]

bsw - build static website

optional arguments:
    -h, --help         show this help message and exit
    -C, --clean        remove existing build folder before building
    -s, --http-server  serve content after build (default port 8000)
```

Nice and simple.

## Getting Started

bsw works primarily on the current directory, and expects a couple of
folders to exist:

* pages
* templates

To get started, we'll need to create these folders and add a base
template (the primary site template) to the *templates* folder.

```
$ mkdir pages
$ mkdir templates
$ echo <<EOF > templates/base.html
> <html>
> <head><title>\$page_title</title></head>
> <body>
> \$page_content
> </body>
> </html>
> EOF
```

bsw will read all the \*.html and \*.htm files inside the `pages` directory
(recursively) and render them using the base template. The rendered pages
will then be saved to the `build` folder (which will be created if needed).

When pages are rendered using templates, the template placeholders
(e.g. `$page_title`) are replaced with page variables (declared like
`<!-- page_title = "my page title" -->`). The special `$page_content`
placeholder is replaced with the page content itself (the body of the
`pages/*.html` file).

Let's create an example page:

```
$ mkdir pages/about
$ echo <<EOF > pages/about/index.html
> <!-- page_title = "about this site" -->
> <h1>About this site</h1>
> <p>This is our example site, built with bsw.</p>
> EOF
```

By naming the file `index.html` and putting that inside a folder names
`about` we can access the page using the prettier URL
`http://localhost:8000/about` (rather than `about.html`).

Now that we have some sample content, we can build the website:

```
$ bsw.py -s
```

The `-s` flag tells bsw to start a web server on port 8000 after building
the site. We can then access our about page via
<a href="http://localhost:8000/about">http://localhost:8000/about</a>.


## Static content

bsw will copy any files in `static/` and `templates/static/` to
`build/static/` (the output root) where they can easily be
referenced by your page or template content.

Static folders are completely optional.


# FAQ

## Why are there two static folders?

`bsw` looks for two static folders:

* static/
* templates/static/

This allows you to keep your template static files separate from your
page static files, making it easier to reuse your template on other sites.

However, the user of either (or both) static folders is completely optional.


## How do I create a template?

Templates are extemely simple. Currently, only one template
(`templates/base.html`) is loaded and it requires only a single tag:

```
$page_content
```

The content from each .html or .htm file in `pages/` is inserted into the
base template at the `$page_content` tag.

Pages can also pass values to the template, for example, you template could
contain the following:

```
<head>
    <title>My Example Blog | $page_title</title>
</head>
```

You can populate the `$page_title` variable for any page by declaring it
in a comment in the page markup, as follows:

```
<!-- page_title = "My first blog post! -->
```

*The only template tag which is required is the `$page_content` tag.*
