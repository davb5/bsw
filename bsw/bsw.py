#!/usr/bin/env python
import argparse
import os
import SimpleHTTPServer
import SocketServer
import sys

import files
import pages
import templates

OUT_DIR = os.path.abspath(os.path.join(".", "build"))


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
        sys.exit()


def build_static_web(clean_build_path):
    file_manager = files.FileManager(OUT_DIR)

    # Check that required paths (e.g. base template) exist before starting
    try:
        file_manager.check_required_paths()
    except IOError as ex:
        print("Error: {0}".format(ex))
        print("Did you remember to create the 'templates' folder and 'base.html' template?")
        sys.exit(1)

    if (clean_build_path):
        print("Cleaning build path...")
        file_manager.clean_build_path()
    file_manager.create_out_dir()

    print("Loading pages...")
    site_pages = pages.collect_pages()
    for page in site_pages:
        page.load_and_parse()

    # Check that any explicit templates exist before rendering
    try:
        templates.check_templates_exist(site_pages)
    except IOError as ex:
        print("Error: {0}".format(ex))
        sys.exit(1)

    print("Rendering pages...")
    for page in site_pages:
        page.render()
    print("Writing pages...")
    pages.write_pages(site_pages, OUT_DIR)

    print("Copying site and template assets...")
    file_manager.copy_template_assets()
    file_manager.copy_site_assets()

    print("Static site build complete.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="bsw - build static website")
    parser.add_argument("-C", "--clean", action="store_true",
                        help="remove existing build folder before building")
    parser.add_argument("-s", "--http-server", action="store_true",
                        help="serve content after build (default port 8000)")
    args = parser.parse_args()

    clean_build_path = False
    if args.clean:
        clean_build_path = True

    build_static_web(clean_build_path)

    if args.http_server:
        serve_content()
