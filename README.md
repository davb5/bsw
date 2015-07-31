# bsw
Build Static Website - a simple static website generator


## Usage (the short version)

```
$ bsw.py
```

As simple as that.


## Usage (the longer version)

bsw works on the current directory. It expects a directory structure
like the following:

```
./
|-- \*pages/ 
    |-- index.html
    |-- about/
        |-- index.html
    |-- project/
        |-- index.html
|-- \*templates/ 
    |-- \*base.html
    |-- static/
        |-- css/
            |-- main.css
        |-- images/
            |-- site_logo.png
|-- static/
    |-- images/
        |-- post_screenshot_example.png
    |-- files/
        |-- example.tar.gz
```

*The paths marked with a &ast; are required.*

Running `bsw.py` will read the main site template from `templates/base.html`
and find all the .htm and .html files in `pages/`. The structure of `pages/`
will be recreated in `build/` (creating `build/` if needed), with each page
rendered using the base template.

Any files in `static/` and `templates/static/` will be copied to
`build/static/`.

By default, existing html pages will always be regenerated (overwritten) but
static files will not.

The static folders are completely optional.


# FAQ

## Why are there two static folders?

`bsw` looks for two static folders:

* static/
* templates/static/

The reason for this is simple - it allows you to keep your template statics
separate from your page/post/site statics. This makes it easier to reuse
your template on other sites. However, the user of either (or both) static
folders is completely optional.


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
