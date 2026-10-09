# Becht Pride campaign landing pages

Standalone implementation of the three October 2026 coworker briefs, prepared
for coworker review. Complete the tracking and privacy items below before
sending ad traffic to these pages.

## Pages and intended public URLs

| Campaign | Public path after deployment | Supported `svc` values |
| --- | --- | --- |
| Remodeling | `/ppc-remodeling` | `home`, `bathroom`, `bathroom-contractor`, `kitchen`, `shower`, `basement` |
| Restoration | `/ppc-restoration` | `water`, `basement`, `sewage`, `fire`, `mold`, `storm` |
| Insurance repairs | `/ppc-insurance` | `insurance`, `works-with-insurance`, `storm`, `hail`, `water`, `fire`, `choose` |

Host: `https://bechtpriderestoration.com`. Unknown or missing `svc` values fall
back to each campaign's default. No raw query text is rendered. All default
copy is present without JavaScript. Campaign pages are independent of the
homepage and are not added to its navigation or the search sitemap.

## Preview and editing

Run `python3 scripts/preview.py --port 3001`, then open the paths above on
`http://127.0.0.1:3001`. The preview server supports extensionless HTML routes.

Content and shared markup: `scripts/build-landing-pages.py`. Run it after
editing to regenerate the three checked-in pages. CSS and browser behavior:
`site-v2/ppc/landing.css` and `site-v2/ppc/landing.js`. Python is an optional
authoring tool, not a production runtime or deployment build dependency.

Cloudflare serves `ppc-remodeling.html` directly at `/ppc-remodeling`, and the
other pages the same way. Existing homepage files and legacy redirects are
unchanged. See [Cloudflare route matching](https://developers.cloudflare.com/pages/configuration/serving-pages/).

## Design and supplied assets

- Shared navy/yellow/Inter brand, independent page layouts, phone-only CTAs.
- Self-hosted Inter Latin variable font and its SIL Open Font License.
- Responsive WebP images with JPEG fallback; original project images retained.
- The supplied Drive folder was read. All service images except the company
  van already had matching-named/equivalent local assets. The van was fetched
  from the supplied folder.
- Bathroom, shower and flooring images are from the existing project gallery.
- Stock service imagery is used as illustrative imagery, not labeled as Becht
  completed projects. Kitchen and basement cards use icons.
- The van image has older phone numbers lower down; its on-page crop shows the
  branding above those numbers. Replace it with an updated vehicle/team photo
  before launch if one is available.
- The supplied fire comparison is shown as one image. A draggable wipe between
  differently framed before/after photographs would imply matching viewpoints.
- Only the three named supplied reviews are included. No aggregate rating,
  review count, unnamed "verified" review, or invented certification is used.

## Conversion setup

All CTA links use `tel:+14632384357` and a `data-cta` placement identifier.
Clicks push a `click_to_call` event into an in-memory `dataLayer`, with
`landing_page`, `service`, `cta_location` and `link_url`. Nothing is transmitted
by this code alone. It does not load tracking services or fabricate conversion
IDs. A clicked phone link is not evidence of a connected call or its duration.

Required from the account manager:

1. Approved Google Ads/GA4/GTM setup OR CallRail/DNI snippet and implementation
   instructions. Avoid running two competing number-swapping systems.
2. Separate call conversion labels for each campaign, forwarding-number setup,
   and duration thresholds (brief suggestions: restoration/insurance 60 seconds,
   remodeling 90 seconds).
3. Consent requirements and approved privacy wording for the final setup.
4. End-to-end testing from real ad visits with tag/debug tooling: visible phone
   numbers AND `tel:` destinations must swap consistently, without duplicate
   click events. Header mobile "Call now" links also need their href replaced.

URL parameters including `gclid`, `gbraid` and `wbraid` are left intact. They
are not copied to persistent storage or sent to a provider by the draft code.

## Confirm or omit before launch

- 24/7 phone answering, live-answer/no-call-center claims and arrival windows.
  These claims are omitted from all visible copy, variants and schema. Published
  office hours remain Mon–Fri 8am–4pm.
- In-house trade/no-subcontractor wording, workmanship guarantees and timelines.
  Current copy promises one point of contact rather than unverified staffing.
- Actual service availability, especially outside the nine listed counties.
  Current copy asks callers to confirm availability for their project/address.
- Free damage inspections versus free repair estimates. The drafts advertise
  free estimates only.
- Roofing/hail scope, Xactimate, on-site adjuster meetings and direct insurance
  billing. Stronger unconfirmed claims are omitted.
- Client/legal review of insurance-page language. No settlement negotiation,
  coverage approval, deductible rebate or legal-right guarantee is promised.
  The more categorical contractor-choice and Indiana-law statements in the
  brief have been softened/omitted pending review.
- Source and approval of supplied reviews and permission to use client photos.
- Replace or approve `/ppc-privacy`. It is explicitly a review draft, not an
  approved policy. Do not launch ads with an unfinished privacy notice.
- Confirm final campaign paths with the account manager and test production
  HTTP 200 behavior after deployment.

## Content references

The supplied briefs are the primary copy source. Safety wording was made more
cautious so people are not instructed to operate electrical equipment in water.

- [Ready.gov flood safety](https://www.ready.gov/floods)
- [Indiana Department of Insurance claim tips](https://secure.in.gov/idoi/consumer-services/insurance-claim-tips)
- [Indiana Department of Insurance property insurance](https://www.in.gov/idoi/consumer-services/types-of-insurance/property-insurance/)

## Verification

Use `python3 scripts/check-landing-pages.py` for generated-page integrity checks
and `node scripts/check-landing-behavior.mjs` for headline, reordering, sticky-call
and tracking-event tests. Review all three pages at desktop and mobile widths.
Performance figures in the briefs are targets, not measured guarantees; live
PageSpeed/field INP and Google call forwarding must be checked after deployment
and after the real tracking setup is installed.

Verified locally on October 9, 2026:

- Static checks passed for all assets, 62 phone links, 22 visible/schema FAQ
  pairs, canonical paths, noindex metadata and absence of forms/navigation.
- All 19 supported service variants and 15 missing/invalid-value cases passed
  the script checks, including safe fallback, card order and unchanged ad IDs.
- Browser review covered desktop, tablet and narrow mobile layouts. All 19
  service variants kept the hero call button on the first mobile screen.
- Fixed the narrow-screen review-strip overflow and checked that the company
  van crop hides its older printed phone numbers.
- Verified the mobile call bar appears after scrolling and hides at the final
  CTA; native FAQ expansion works; no browser errors were reported.
- All three clean landing paths, the privacy draft, shared CSS/JS and the
  existing homepage returned HTTP 200 from the local preview server.

No real phone call was placed and no ad conversion was transmitted during QA.
