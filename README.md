# Becht Pride Restoration

Agency repository for the Becht Pride Restoration and Remodeling website.

The website uses HTML, CSS, and vanilla JavaScript. It has no framework,
package dependencies, or build step.

## Website files

The active, deployable website is in **`site-v2/`**. This directory contains
the homepage, service pages, styles, JavaScript, images, redirects, sitemap,
robots.txt, and 404 page. The repository root also contains older supporting
files; publish `site-v2/` as the website root.

## Local preview

From the repository root:

```sh
python3 -m http.server 3000 --bind 127.0.0.1 --directory site-v2
```

Open <http://127.0.0.1:3000/>.

## Cloudflare Pages settings

When setting up a Git-connected Pages project, use:

| Setting | Value |
| --- | --- |
| Repository | `alphadogagency/Becht-Pride-Restoration` |
| Production branch | `main` |
| Framework preset | None |
| Build command | Leave blank; no build is required |
| Build output directory | `site-v2` |
| Root directory | Repository root (leave the default) |

The existing `bechtpriderestoration` Cloudflare Pages project was connected to
this repository on October 9, 2026. Production branch: `main`; automatic
deployments: enabled. Pushing to `main` publishes `site-v2/` to
<https://bechtpriderestoration.com/> when the deployment succeeds.

Review local changes before committing and pushing to production.

## Campaign landing pages

The three standalone campaign pages are `/ppc-remodeling`, `/ppc-restoration`
and `/ppc-insurance`. They are separate from the homepage and its navigation.
See [the landing-page notes](docs/landing-pages.md) for pending launch details,
tracking setup and editing instructions.

For previews with the same clean URLs as Cloudflare:

```sh
python3 scripts/preview.py --port 3001
```

## Contact form

The contact form in `site-v2/js/main.js` submits to the existing ADA Landings
service. Submitting it can create a real lead and send notifications, including
from local previews.

## Repository import

This repository starts with a snapshot of the supplied website files. Previous
Git history and internal credential-bearing notes are intentionally excluded.
