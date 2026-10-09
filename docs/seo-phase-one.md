# Becht Restoration — Phase 1 SEO

Source: Kyle's `Becht-Restoration-SEO.md`, attached to the October 3, 2026
“Becht MD” email. Kyle's October 9 reply confirms that the agency should supply
the missing copy. Bryan requested publication on the existing live website for
review. There is no staging-site deliverable.

## Scope and page structure

- Rewrite metadata and headings, structure service content, add FAQs, improve
  internal links and navigation, and generate shared structured data.
- Build `/service-areas/` and the 14 requested city pages, each at
  `/service-areas/[city]-in/`.
- Preserve the existing restoration, remodeling, and handyman offerings.
- Use the existing ADA Landings form endpoint, with the originating city
  included in the message sent to the existing lead system.
- Publish a sitemap and provide a URL inventory for rank tracking and review.
- Leave campaign landing pages independent and `noindex`.

The result has **31 canonical URLs**: homepage, 15 services, Service Areas hub,
and 14 city pages. See [the metadata inventory](seo-url-inventory.csv) and
[the URL list for Kenny](seo-rank-tracking-urls.txt).

## Decisions that reconcile the brief

1. **Two remodeling pages and duplicate consolidation.** The former
   `/services/remodeling` overlaps with `/services/home-remodeling`. Both old
   spellings now lead directly to `/services/home-remodeling/`. A distinct
   `/services/kitchen-bathroom-remodeling/` page covers the room-specific intent
   and retains examples from the existing bathroom gallery. This provides the
   two remodeling destinations and two sets of five FAQs requested by the
   brief. It is a replacement destination within the service cleanup, in
   addition to the 15 requested location URLs.
2. **Reconstruction links.** Restoration pages point to the reconstruction
   section of the home-remodeling page, which describes the existing rebuild
   service. No additional city-by-service or reconstruction-page matrix was
   introduced. Handyman/remodeling Related Services sections stay within that
   group; shared navigation still exposes the whole business.
3. **Title length.** The supplied long example titles conflict with “under 60
   characters.” Titles are unique and under 60, preserving the service/city
   intent with the concise brand “Becht Pride.” Full branding appears in page
   content and structured data. Meta descriptions are 140–155 characters.
4. **URL format.** All organic canonical pages now use trailing slashes.
   Previous extensionless and `.html` paths, duplicate URLs, and known legacy
   paths redirect directly to the final destination. Query strings are
   preserved. Cloudflare serves directory `index.html` files at slash paths;
   see [Cloudflare route matching](https://developers.cloudflare.com/pages/configuration/serving-pages/).
5. **Business identity and hours.** All pages identify the same Indianapolis
   business and street address. City pages change `areaServed`, not the office
   location; no fictitious city branches are represented. Emergency availability
   is 24/7, with weekday office hours displayed separately.
6. **FAQs.** Five visible questions and matching `FAQPage` entries appear on
   each of the four restoration and two remodeling pages. Other service pages
   have two relevant FAQs. Google retired FAQ rich results in May 2026, so
   markup validity is checked separately from rich-result eligibility.
   [Google's documentation update](https://developers.google.com/search/updates#may-2026).
7. **Testimonials.** New city pages do not assign a customer's project to a
   city without evidence. The brief makes city testimonials conditional on
   availability. The homepage uses the three named reviews previously supplied
   for the campaign pages, without inferred cities or aggregate rating claims.

## Research and editorial approach

Initial competitor sampling covered Guardian Angel Restoration, Independent
Restoration Services, and Premier Restoration. Their public pages emphasize
emergency contact, local service coverage, insurance documentation, and the
connection between cleanup and rebuilding. Those themes overlap Becht's
existing services and the brief. Competitor wording, response guarantees,
certifications, and reviews were not imported.

- https://www.guardianangelrestoration.com/services/
- https://irs-247.com/locations/indianapolis
- https://premier911.com/

This is a qualitative content/intent review, not a measured keyword-volume or
rankings report. Search Console performance data was not available during the
initial research. The city pages target restoration plus city intent and link
to the service pages for detailed explanations. There are no keyword-stuffed
city/service permutations.

Each city has **200–300 words of independently written local introduction**.
The source is stored with the city record and linked visibly on its page.
Research supports local context, not claims about Becht's job history. Copy
avoids invented projects, guarantees, city-specific customer experiences,
arrival times, and insurance outcomes.

| City | Local context | Source |
| --- | --- | --- |
| Indianapolis | Historic-property lookup and property-specific repair planning | [City historic district lookup](https://www.indy.gov/workflow/find-your-historic-district) |
| Carmel | Groundwater, local soil drainage, and basement moisture | [Carmel Engineering](https://www.carmel.in.gov/government/departments-services/engineering) |
| Fishers | Distinct White River, Mud Creek, and Geist/Fall Creek drainage areas | [City stormwater plan](https://fishersin.gov/wp-content/uploads/2024/01/City-of-Fishers-Stormwater-Masterplan-December-2018-1-1.pdf) |
| Noblesville | White River corridor, Forest Park, and the historic downtown | [City trails](https://www.noblesville.in.gov/715/Trails) |
| Westfield | Grand Junction and downtown context | [Grand Junction Plaza](https://www.westfieldin.gov/Facilities/Facility/Details/Grand-Junction-Plaza-19) |
| Greenwood | Localized flooding and older-neighborhood drainage | [City comprehensive-plan stormwater section](https://www.greenwood.in.gov/egov/documents/1726152356_91416.pdf) |
| Zionsville | Village and surrounding residential/rural areas | [Town administration overview](https://zionsville-in.gov/278/Mayor-Administration) |
| Avon | White Lick Creek, Abner Creek, and Clarks Creek watersheds | [Town public works notices](https://www.avonindiana.gov/570/Public-Works-Public-Notices) |
| Plainfield | White Lick Creek high-water context | [Town parks and trails FAQ](https://www.townofplainfield.com/m/faq?cat=15) |
| Brownsburg | Runoff, local drainage, and stormwater management | [Town stormwater program](https://www.brownsburg.org/277/Stormwater) |
| Franklin | Youngs Creek, greenway, and downtown context | [City parks guide](https://www.franklin.in.gov/egov/documents/1693935472_78212.pdf) |
| McCordsville | Old Town, McCord Square, and neighborhood types | [Town comprehensive plan](https://www.mccordsville.org/egov/documents/1741964263_22746.pdf) |
| Fortville | Established town center and existing housing | [Town comprehensive plan](https://cdn.townweb.com/fortvilleindiana.org/wp-content/uploads/2021/05/EnvisionFortvilleFinal.pdf) |
| Anderson | West Central and West Eighth Street historic districts | [City preservation commission](https://www.cityofanderson.com/139/Historical-Cultural-Preservation-Commiss) |

Business services and contact details come from the existing site and project
records. The street address and Google profile link were cross-checked against
the [existing Residential Services listing](https://reviews.birdeye.com/becht-pride-residential-services-166401876604184).
The Facebook URL is from the original company website export. These are
identity references, not a claim that a profile's ownership or status was audited.

Safety and insurance wording was checked against [EPA mold guidance](https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home)
and [Indiana Department of Insurance claim guidance](https://www.in.gov/idoi/consumer-services/insurance-claim-tips/).
No health diagnosis or promise of insurance coverage is made. Google's
[helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
informed the emphasis on useful property-specific explanations.

## Editing and verification

- Homepage sections: `content/seo/home.html`.
- City introductions and source links: `content/seo/cities.json`.
- Service descriptions and FAQs: `scripts/seo_services.py`.
- Shared head, navigation, footer, forms, schema, and page layouts:
  `scripts/build-seo-pages.py`.
- Additional styles: `site-v2/css/seo.css`; browser behavior:
  `site-v2/js/main.js`.

Run:

```sh
python3 scripts/build-seo-pages.py
python3 scripts/check-seo-pages.py
node scripts/check-seo-form.mjs
python3 scripts/check-landing-pages.py
node scripts/check-landing-behavior.mjs
python3 scripts/preview.py --port 3002
```

The generator writes deployable HTML, redirects, sitemap, and inventories.
Python is an authoring dependency only. No runtime framework or deployment
build step is introduced. Edit the sources and regenerate, rather than editing
the generated HTML directly.

Static checks cover all canonical pages, assets, links and anchors, duplicate
metadata, length requirements, heading counts, forms, visible/schema FAQ
agreement, city word counts, inbound links, and redirect destinations. Form
tests execute the actual shipped handler against an isolated mock API and
cover all city payloads, failures, timeout, retry, and duplicate submissions.
They never call the live lead API. Existing campaign regression checks remain
part of verification.

## Account-dependent completion

The available browser prompted for Google reauthentication when opening Search
Console. Sitemap submission and individual indexing requests require an
authenticated account with access to this property. They are separate from
publishing the sitemap and making the pages discoverable through internal links.

The rank-tracking URL list is prepared for Kenny. No email was sent by this
implementation. Publication and final live verification are recorded below
when completed.

## Pre-publication verification — October 9, 2026

- Static crawl passed: 31 canonical pages, 48 visible/schema FAQ pairs,
  all 14 city introductions, and 294 redirect rules.
- Local HTTP crawl passed 329 checks, including canonical URLs, campaign
  routes, redirects with query strings, shared assets, and a true 404 response.
- Form-handler tests passed with isolated API responses for all 14 city
  payloads, invalid fields, duplicate submission, failures, timeout, and retry.
  No real lead was submitted; production delivery/notifications were not tested.
- Existing campaign content and behavior regression checks passed. Campaign
  files and assets were unchanged.
- Browser review covered desktop, tablet, all 14 city pages at 375px, mobile
  navigation/Escape, estimate anchors, required-field validation, and an FAQ
  disclosure. No horizontal overflow remained. The homepage, service page,
  remodeling page, city page, and service-area hub were visually inspected.
- JavaScript syntax and Git whitespace checks passed.
