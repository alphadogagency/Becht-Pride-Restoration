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

Verify a preview before publishing to the production domain,
<https://bechtpriderestoration.com/>. Creating or pushing to this repository
does not itself connect it to Cloudflare or deploy the website.

Cloudflare documents that existing Direct Upload projects cannot switch to
built-in Git integration. To retain such a project, GitHub Actions can publish
`site-v2/` with Wrangler. Confirm the target project's setup before connecting
Git or enabling automatic production deployments.

- [Direct Upload documentation](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Deploy with GitHub Actions](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)

## Contact form

The contact form in `site-v2/js/main.js` submits to the existing ADA Landings
service. Submitting it can create a real lead and send notifications, including
from local previews.

## Repository import

This repository starts with a snapshot of the supplied website files. Previous
Git history and internal credential-bearing notes are intentionally excluded.
