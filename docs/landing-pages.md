# Becht Pride campaign landing pages

Standalone implementation of the three October 2026 coworker briefs, published
for coworker review. Complete the requested call-conversion tracking before
sending ad traffic to these pages. The existing Becht Pride privacy policy is
linked from all three footers.

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

Section 10 of all three briefs requests Google Ads website-call conversions
and secondary call-click events. GTM is an implementation option, not an
additional requirement. CallRail is conditional on the client already using it.

The main company site, `bechtpride.com`, embeds `GTM-MWJM322`. Its public
container includes Google Ads `AW-937096300`, GA4 `G-GEBP7JLS1H`, and call-click
events. This does not establish which account or conversion actions Jordan
wants for the restoration campaigns. No Google Ads, GTM or CallRail installation
was found in the 22 published restoration-site HTML pages or their source
scripts; Cloudflare adds its own analytics beacon.

The remaining input from the account manager is the correct Google Ads account
and the website-call conversion labels/snippets for these three campaigns.
Confirm the call-duration thresholds when configuring those conversions (brief
suggestions: restoration/insurance 60 seconds; remodeling 90 seconds). Reuse
the existing setup only if it is the intended setup for these campaigns.

Then test real ad visits with tag/debug tooling: visible phone numbers AND
`tel:` destinations must swap consistently, without duplicate click events.
Header mobile "Call now" links also need their href replaced. Apply the briefs'
conditional consent instructions if a consent banner is used.

URL parameters including `gclid`, `gbraid` and `wbraid` are left intact. They
are not copied to persistent storage or sent to a provider by the draft code.

## Existing-site answers and scope

Check existing site content before asking the account manager to supply facts
again. Separate explicit brief requirements from optional suggestions.

- [Existing privacy policy](https://bechtpride.com/privacy-policy/): its scope
  includes Becht Pride subsidiaries/affiliates and other owned or controlled
  sites that link to it. All landing footers now link directly to it; the draft
  `/ppc-privacy` notice is retired and that route redirects to the existing policy.
- [Water damage page](https://bechtpriderestoration.com/services/water-damage):
  explicitly states 24/7 call answering, an in-house remodeling team, insurance
  coordination and free estimates. These are already published business facts,
  rather than unanswered questions for this build. Office hours are separate.
- [Home remodeling page](https://bechtpriderestoration.com/services/home-remodeling):
  explicitly states in-house plumbing, electrical, tiling and finishing, plus
  free consultations and detailed estimates.
- The homepage lists the nine service counties. Outer-area coverage, free
  inspections, response-time promises, Xactimate, direct insurance billing,
  warranties, financing and the unnamed review remain omitted. The briefs
  permit unresolved `[CONFIRM]` claims to be removed; these optional additions
  are not new work or blockers.
- The insurance brief requests client review of the final copy. Handle that
  through the current page-review process, without adding unrelated services.

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
