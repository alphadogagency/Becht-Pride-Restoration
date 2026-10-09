#!/usr/bin/env python3
"""Local static preview with Cloudflare Pages-style extensionless HTML routes."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'site-v2'


class Handler(SimpleHTTPRequestHandler):
    def apply_redirect(self):
        requested = urlsplit(self.path)
        for line in (ROOT / '_redirects').read_text().splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            source, target, status = line.split()
            matches = requested.path.startswith(source[:-1]) if source.endswith('*') else requested.path == source
            if matches:
                if requested.query and '?' not in target:
                    target += '?' + requested.query
                self.send_response(int(status))
                self.send_header('Location', target)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return True
        return False

    def do_GET(self):
        if not self.apply_redirect():
            super().do_GET()

    def do_HEAD(self):
        if not self.apply_redirect():
            super().do_HEAD()

    def translate_path(self, path):
        translated = Path(super().translate_path(path))
        if not translated.exists() and not Path(urlsplit(path).path).suffix:
            candidate = Path(str(translated) + '.html')
            if candidate.is_file():
                return str(candidate)
        return str(translated)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=3001)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(ROOT)))
    print(f'Preview: http://127.0.0.1:{args.port}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
