# Children evidence review - Codex, 13 October 2026

Read both whole-project audits. The fixed 43/18/24/15% distribution has no defensible provenance and must not affect calculator results.

## Actual public evidence retained

Ipsos / Royal Foundation general-population tables are already retained in `archive/v3_legacy/v3/sources/ipsos-parenthood-2025.pdf`. SHA256: `847fcaa6f17e40560cf4d3a0ac8d233ae7a45851541b90d6f644c4f2c7daf4fd`; size 37,970,632 bytes; 205 pages. The online source is [the official Ipsos PDF](https://www.ipsos.com/sites/default/files/ct/news/documents/2026-01/j25-023254-tabs-draft-IntUse-gp-wtd-v9.tab_.pdf). The [article's technical note](https://www.ipsos.com/en-uk/95-public-believe-early-childhood-crucial-shaping-persons-future-yet-many-parents-struggle-modern) identifies the nationally weighted general-population sample of 4,672 UK adults aged 16+. The additional parent boost must not supply the population denominator.

`public/evidence/children-ipsos-2025.json` retains selected verified count rows and exact questions. `scripts/data/children_inspect.py` reproduces text inspection and the source hash from the retained/downloaded PDF. Neither file invents age-by-sex joint cells.

- QD6, Table 636, PDF page 172: counts under-18 children for whom the respondent has parental responsibility and who live with the respondent permanently or temporarily. Actual weighted counts: no children in this narrower question 3,226; one 672; two 626; three 126; four-plus 21; any 1,446. Sex and age marginals are present separately. Counts are rounded and need not sum exactly.
- QD9, Table 651, PDF page 175: under-18 children not currently living with respondent; yes 489, no 4,164, nonresponse 19. These overlap with QD6 parents. Adding parent counts overstates unique adults.
- QD10, Table 656, PDF page 176: adult children explicitly includes those living elsewhere; net yes 1,977. With-me and elsewhere responses overlap, and neither can be added to QD6/QD9 to identify unique parents.

## Scope and decision

QD6 can support a clearly labelled **children under 18 who live with you, including temporary stays** reference. It is broader than permanent-household-only children, but it excludes under-18 children living elsewhere and grown-up children. Its wording does not restrict to biological children; adoption is not separately documented, so do not certify an adoption-specific share.

The PDF provides separate age and sex marginals rather than their joint intersection. Its youngest band includes 16-17-year-olds. It therefore does not establish the requested all-adult, sex-and-age-conditioned parenthood distribution. A model using the age marginals for both sexes would be an explicit proxy requiring that disclosure; multiplying separate age and sex rates would not create measured joint data.

Until a suitable joint table is obtained, remove the old multiplier and explicitly show selected parenthood requirements as **not counted in the estimate**. Keep original source links and the useful reference data discoverable. Do not claim no dependent children at home means no children anywhere. Do not fabricate co-parent counts.

## ONS household fallback checked

The ONS dictionary identifies `hh_dependent_children` as a household-level variable. The person-level custom API rejected it (400: variable does not exist). It also rejected `adult_lifestage` and `adult_lifestage_9a` in tested usual-resident queries. More importantly, the [adult-lifestage definition](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/adultlifestage) does not distinguish children for all people aged 65+ and excludes communal residents. Its complement cannot be assigned to all adults as childlessness. Family and household totals must never be relabelled as parent counts.

This is a reproducible evidence limitation, not proof that no suitable source exists. UK Data Service licensed microdata remain a route to broader parenthood modelling, subject to obtaining the actual data and verifying variables, weights, and missing responses.
