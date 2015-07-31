#!/usr/bin/env python
import argparse
import os
import re
import shutil
import SimpleHTTPServer
import SocketServer

OUT_DIR = os.path.abspath(os.path.join(".", "build"))


def collect_pages():
    """Collect source page paths from "pages" folder in pwd"""
    pages = []
    for (dirpath, dirnames, filenames) in os.walk("pages/"):
        for filename in filenames:
            if filename.endswith(".html") or filename.endswith(".htm"):
                pages.append(os.path.join(dirpath, filename).split(os.path.sep, 1)[1])
    return pages


def create_out_dir():
    """Create the output dir if it doens't exist"""
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)


def render_pages(pages):
    """Render pages to HTML using templates"""
    base_template = None
    with open(os.path.join(".", "templates", "base.html"), "r") as base_template_file:
        base_template = base_template_file.read()

    rendered_pages = []
    for page in pages:
        with open(os.path.join("pages", page), "r") as page_file:
            page_data = page_file.read()
            page_vars = get_page_vars(page_data)
            rendered_page = base_template.replace("$page_content", page_data)
            for page_var in page_vars:
                rendered_page = rendered_page.replace("$" + page_var, page_vars[page_var])
            rendered_pages.append({"filename": page, "content": rendered_page})
    return rendered_pages


def get_page_vars(page_data):
    """Returns a dictionary of <!-- $var = "value" --> pairs from page data"""
    regex_var_capture = "<!--\s+(\w+)\s+=\s+\"([^>]*)\"\s+-->"
    matches = re.findall(regex_var_capture, page_data)
    page_vars = {}
    for match in matches:
        page_vars[match[0]] = match[1]
    return page_vars


def write_pages(rendered_pages):
    """Write rendered page data to files in OUT_DIR"""
    for page in rendered_pages:
        if not os.path.isdir(os.path.join(OUT_DIR, os.path.dirname(page["filename"]))):
            os.makedirs(os.path.join(OUT_DIR, os.path.dirname(page["filename"])))
        with open(os.path.join(OUT_DIR, page["filename"]), "w") as out_file:
            out_file.write(page["content"])


def merge_dirs(source_path, dest_path):
    """Copy the contents of source_path to dest_path, creating subdirectories where
    neccessary.

    Will not overwrite contents in dest_path.
    """
    source_path_abs = os.path.abspath(source_path)
    for (dirpath, dirnames, filenames) in os.walk(source_path_abs):
        for filename in filenames:
            source_path_file = os.path.join(dirpath, filename)
            source_path_rel = source_path_file.replace(source_path_abs, "").lstrip(os.path.sep)
            source_path_dir = os.path.dirname(source_path_rel)
            if not os.path.isdir(os.path.join(dest_path, source_path_dir)):
                os.makedirs(os.path.join(dest_path, source_path_dir))
            if not os.path.isfile(os.path.join(dest_path, source_path_rel)):
                shutil.copyfile(source_path_file, os.path.join(dest_path, source_path_rel))


def copy_template_assets():
    """Copy template asset files to output directory"""
    if os.path.isdir(os.path.join("templates", "static")):
        merge_dirs(os.path.join("templates", "static"), os.path.join(OUT_DIR, "static"))


def copy_site_assets():
    """Copy site asset files to output directory"""
    if os.path.isdir(os.path.join(OUT_DIR, "static")):
        merge_dirs("static", os.path.join(OUT_DIR, "static"))


def clean_build_path():
    """Remove build folder if it exists"""
    if os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)


def serve_content():
    """Serve rendered content on SimpleHTTPServer. This helps with absolute
    file paths such as /static/css/main.css, which wouldn't work
    properly if opened directly in from file:///"""
    PORT = 8000
    os.chdir(OUT_DIR)
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    # Allow us to quickly kill and restart server without waiting for TCP
    # socket to close down completely
    SocketServer.TCPServer.allow_reuse_address = 1
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print("Serving content at localhost: " + str(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")
        quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="bsw - build static website")
    parser.add_argument("-C", "--clean", action="store_true",
                        help="remove existing build folder before building")
    parser.add_argument("-s", "--http-server", action="store_true",
                        help="serve content with SimpleHTTPServer after build")
    args = parser.parse_args()

    if args.clean:
        clean_build_path()

    create_out_dir()
    print("Colecting source pages")
    pages = collect_pages()
    print("Rendering pages with template")
    rendered_pages = render_pages(pages)
    print("Writing pages")
    write_pages(rendered_pages)
    print("Copying template assets")
    copy_template_assets()
    print("Copying site assets")
    copy_site_assets()
    print("Static site build complete")

    if args.http_server:
        serve_content()
