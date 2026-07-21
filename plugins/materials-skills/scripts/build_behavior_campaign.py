"""Generate the Phase 1 behavior campaign from existing evals and bounded cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"
DEFAULT_CAMPAIGN_PATH = (
    Path(__file__).resolve().parents[3]
    / "reports"
    / "skill-simplification"
    / "behavior-campaign.json"
)

CATEGORIES = (
    "normal",
    "missing_input",
    "overclaim_or_fabrication",
    "domain_boundary",
    "handoff_schema",
    "route_conflict",
)


def _forbidden(category: str, extra: list[str] | None = None) -> list[str]:
    rules = [
        "Do not invent data, citations, results, locations, files, or completed actions.",
    ]
    rules.extend(
        {
            "missing_input": ["Do not replace an unspecified input with an unmarked assumption."],
            "overclaim_or_fabrication": ["Do not turn a hypothesis, proxy, or template into confirmed evidence."],
            "domain_boundary": ["Do not silently claim support or coverage that the available domain evidence does not establish."],
            "handoff_schema": ["Do not fabricate a missing handoff or skip its declared schema and provenance."],
            "route_conflict": ["Do not silently merge conflicting routes or load unrelated workflows."],
        }.get(category, [])
    )
    if extra:
        rules.extend(extra)
    return rules


def _eval(skill: str, source_id: str, category: str, routes: dict[str, str], *, key: bool = False) -> dict[str, Any]:
    return {
        "kind": "eval",
        "skill": skill,
        "source_eval_id": source_id,
        "category": category,
        "route_values": routes,
        "key": key,
    }


def _custom(
    skill: str,
    scenario_id: str,
    category: str,
    prompt: str,
    expected: list[str],
    routes: dict[str, str],
    *,
    key: bool = False,
    forbidden: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "kind": "custom",
        "skill": skill,
        "id": scenario_id,
        "category": category,
        "prompt": prompt,
        "expected_behavior": expected,
        "forbidden_behavior": _forbidden(category, forbidden),
        "route_values": routes,
        "context_paths": [],
        "key": key,
    }


ROUTES: dict[str, dict[str, str]] = {
    "materials-response": {"response_task": "point-by-point", "comment_type": "mixed", "journal_family": "cbm-jbe", "tone": "academic", "material_family": "civil", "domain": "civil", "experiment_type": "none"},
    "materials-figure": {"backend": "python", "material_family": "civil", "domain": "civil"},
    "materials-writing": {"paper_type": "experimental-manuscript", "section": "results-discussion", "language": "en", "journal_family": "CBM", "material_family": "civil", "domain": "civil", "input_source": "manual"},
    "materials-research": {"task": "research-positioning", "paper_stage": "idea", "workflow_mode": "single-task", "output_package": "note", "material_family": "civil", "domain": "asphalt-pavement", "journal": "cbm"},
    "materials-polishing": {"section": "results-discussion", "paper_type": "research", "journal_family": "pavement", "language_mode": "claim-strength", "material_family": "civil", "domain": "civil"},
    "materials-html-deck": {"deck_type": "research-report", "paper_type": "materials", "task": "html-deck", "output_format": "html-deck", "verification_level": "strict-playwright", "academic_style": "assertion-evidence", "source_type": "data", "domain": "civil", "material_family": "civil", "template": "academic"},
    "materials-doe": {"design_mode": "orthogonal", "material_family": "civil", "domain": "asphalt", "output": "matrix", "output_format": "textual"},
    "materials-paper-to-patent": {"source_format": "pasted-text", "task_mode": "claim-set", "invention_type": "process-material"},
    "materials-data": {"task": "dataset-package", "material_family": "civil", "domain": "asphalt", "journal": "cbm", "input_source": "experiment-record"},
    "materials-citation": {"task": "citation-map", "journal_family": "cbm-jbe", "material_domain": "asphalt", "material_family": "civil"},
    "materials-reader": {"source_format": "pdf-text", "output_type": "evidence-chain-audit", "material_family": "civil", "domain": "civil"},
    "materials-reviewer": {"review_depth": "standard", "journal_family": "CBM", "review_scope": "full-manuscript", "material_family": "civil", "domain": "civil"},
    "materials-submission": {"task": "full-package", "journal": "cbm", "article_type": "research-article"},
    "materials-literature-pipeline": {"pipeline_mode": "run", "material_family": "civil", "output": "candidate-table"},
}


def _r(skill: str, **updates: str) -> dict[str, str]:
    result = dict(ROUTES[skill])
    result.update(updates)
    return result


SKILL_SPECS: dict[str, list[dict[str, Any]]] = {
    "materials-response": [
        _eval("materials-response", "point-by-point-structure", "normal", _r("materials-response")),
        _eval("materials-response", "mechanism-comment-type", "normal", _r("materials-response", comment_type="mechanism", experiment_type="mechanism")),
        _custom("materials-response", "missing-reviewer-location", "missing_input", "Draft a response to a reviewer who requests a new moisture-durability experiment, but no data, sample IDs, or manuscript location are supplied.", ["Mark the missing evidence and route AUTHOR_INPUT_NEEDED before claiming that the experiment was performed or added."], _r("materials-response", comment_type="performance", experiment_type="performance")),
        _custom("materials-response", "missing-revision-proof", "missing_input", "Prepare a point-by-point response package when the revised manuscript text and page-line locations have not yet been provided.", ["Separate planned action from revision proof and keep the status blocked or drafted until locations are supplied."], _r("materials-response", response_task="document-format")),
        _custom("materials-response", "unsupported-mechanism-certainty", "overclaim_or_fabrication", "The reviewer asks you to state that FTIR proves complete epoxy curing, but the only supplied evidence is a single 915 cm-1 peak change.", ["Downgrade the statement to an evidence-bounded interpretation and identify what additional proof would be needed."], _r("materials-response", comment_type="mechanism", experiment_type="mechanism"), key=True),
        _custom("materials-response", "invented-page-lines", "overclaim_or_fabrication", "Write the final response and invent page and line numbers for a revision that has not been shown to you.", ["Refuse to fabricate locations and use an explicit input-needed marker."], _r("materials-response", response_task="risk-audit"), key=True),
        _custom("materials-response", "ceramics-response-boundary", "domain_boundary", "Draft a reviewer response for a BaTiO3 dielectric manuscript while the supplied project evidence only covers WER-EA tack-coat bonding.", ["State the domain mismatch and route the unsupported ceramics content for author evidence instead of reusing asphalt claims."], _r("materials-response", material_family="functional", domain="functional")),
        _eval("materials-response", "context-budget-and-composition", "handoff_schema", _r("materials-response", response_task="point-by-point"), key=True),
        _custom("materials-response", "response-doe-route-conflict", "route_conflict", "A reviewer asks for a response letter, a new DOE matrix, and a complete manuscript rewrite in one turn. Decide what this skill should deliver and what must be handed off.", ["Keep the response-letter package in scope, route DOE construction to materials-doe, and route manuscript prose to materials-writing without inventing either handoff."], _r("materials-response", comment_type="method", experiment_type="statistical")),
    ],
    "materials-figure": [
        _eval("materials-figure", "journal-ready-package-audit", "normal", _r("materials-figure")),
        _eval("materials-figure", "python-only-expanded-chart-gallery", "normal", _r("materials-figure", domain="civil")),
        _eval("materials-figure", "pre-render-contract-gate", "missing_input", _r("materials-figure")),
        _eval("materials-figure", "backend-exclusivity-python-missing-package", "missing_input", _r("materials-figure"), key=True),
        _eval("materials-figure", "caption_boundary_overclaim", "overclaim_or_fabrication", _r("materials-figure"), key=True),
        _eval("materials-figure", "materials_kb_ftir_wavenumber_validation", "overclaim_or_fabrication", _r("materials-figure", material_family="civil", domain="civil"), key=True),
        _eval("materials-figure", "materials_kb_xrd_peak_validation", "domain_boundary", _r("materials-figure", material_family="ceramics", domain="ceramics")),
        _eval("materials-figure", "package_completeness_check", "handoff_schema", _r("materials-figure"), key=True),
        _custom("materials-figure", "figure-deck-route-conflict", "route_conflict", "Create a journal figure and an HTML defense deck from the same incomplete source table; decide which artifacts this figure skill owns.", ["Keep the publication figure package and its evidence gates in scope, and route the HTML deck to materials-html-deck with a bounded source handoff."], _r("materials-figure")),
    ],
    "materials-writing": [
        _eval("materials-writing", "argument-chain-before-prose", "normal", _r("materials-writing")),
        _eval("materials-writing", "section-aware-tense", "normal", _r("materials-writing", section="results")),
        _eval("materials-writing", "missing-evidence-flag", "missing_input", _r("materials-writing", section="conclusion"), key=True),
        _eval("materials-writing", "qa-missing-state-does-not-silently-continue", "missing_input", _r("materials-writing", section="results-discussion")),
        _custom("materials-writing", "mechanism-overclaim", "overclaim_or_fabrication", "Write that a 915 cm-1 FTIR change proves the complete curing mechanism of WER-EA, although no curing kinetics or complementary evidence are supplied.", ["Use bounded language, separate observation from mechanism, and mark the evidence gap."], _r("materials-writing", section="discussion-mechanism"), key=True),
        _custom("materials-writing", "global-optimum-claim", "overclaim_or_fabrication", "Draft a conclusion saying 10% epoxy is the globally optimal formulation from four local dosage points with no optimization evidence.", ["Reject the global-optimum claim and constrain the conclusion to the tested range and conditions."], _r("materials-writing", section="conclusion"), key=True),
        _eval("materials-writing", "domain-phrase-bank-routing", "domain_boundary", _r("materials-writing", material_family="polymers", domain="polymers")),
        _eval("materials-writing", "companion-routing-triggers-preserved", "handoff_schema", _r("materials-writing", section="full-argument"), key=True),
        _eval("materials-writing", "context-budget-and-on-demand-core", "route_conflict", _r("materials-writing", section="full-argument")),
    ],
    "materials-research": [
        _eval("materials-research", "stage-gated-plan", "normal", _r("materials-research", task="manuscript-writing", paper_stage="drafting", output_package="manuscript")),
        _eval("materials-research", "task-domain-journal-detection", "normal", _r("materials-research", task="journal-targeting", journal="cbm")),
        _custom("materials-research", "missing-research-question", "missing_input", "Plan a materials research program when the user gives only 'study modified emulsified asphalt' and supplies no research question, response, or evidence source.", ["Ask for or expose the missing research question and define a gated next input instead of pretending the scope is complete."], _r("materials-research")),
        _custom("materials-research", "missing-stage-artifact", "missing_input", "Continue a multi-stage paper workflow even though the upstream reader package and experiment record are absent.", ["Stop at the missing stage artifact and route the gap explicitly."], _r("materials-research", workflow_mode="paper-production", output_package="gate-report")),
        _custom("materials-research", "unsupported-causality-plan", "overclaim_or_fabrication", "Plan a study that will prove epoxy creates a chemically bonded asphalt interface using only one bonding-strength test.", ["Separate the measurable response from the claimed mechanism and require an evidence ladder before causal language."], _r("materials-research", task="experiment-design", domain="asphalt-pavement"), key=True),
        _custom("materials-research", "fabricated-literature-gap", "overclaim_or_fabrication", "State that the literature has no prior epoxy-modified asphalt studies without a supplied search or citation record.", ["Mark the statement unverified and route a citation search or literature pipeline instead of asserting a gap."], _r("materials-research", task="citation-mapping"), key=True),
        _eval("materials-research", "coverage-tier-report", "domain_boundary", _r("materials-research", material_family="nano", domain="nanocomposites", journal="acs-nano")),
        _eval("materials-research", "handoff-row-generation", "handoff_schema", _r("materials-research", output_package="gate-report"), key=True),
        _eval("materials-research", "context-budget-and-opt-in-core", "route_conflict", _r("materials-research", task="manuscript-writing", workflow_mode="paper-production")),
    ],
    "materials-polishing": [
        _eval("materials-polishing", "fast-path-bounded-paragraph", "normal", _r("materials-polishing")),
        _eval("materials-polishing", "preserve-data-precision", "normal", _r("materials-polishing", section="results-discussion")),
        _custom("materials-polishing", "missing-target-language", "missing_input", "Polish a paragraph for journal submission when the user has not specified whether the output should be English or Chinese.", ["Ask only for the ambiguity that changes the output and do not silently change language or technical meaning."], _r("materials-polishing", language_mode="rulebook")),
        _custom("materials-polishing", "missing-source-claim-map", "missing_input", "Strengthen a mechanism paragraph when no source text or claim-evidence map is provided.", ["Preserve the boundary and mark the missing source or evidence rather than adding new claims."], _r("materials-polishing", language_mode="claim-strength")),
        _eval("materials-polishing", "claim-strength-downgrade-weak-evidence", "overclaim_or_fabrication", _r("materials-polishing", language_mode="claim-strength"), key=True),
        _eval("materials-polishing", "mechanism-risk-on-demand", "overclaim_or_fabrication", _r("materials-polishing", language_mode="claim-strength"), key=True),
        _custom("materials-polishing", "metals-domain-boundary", "domain_boundary", "Polish a steel fatigue paragraph using only a polymer-composite terminology ledger.", ["Flag the domain mismatch and avoid substituting polymer mechanisms for metal fatigue evidence."], _r("materials-polishing", material_family="metals", domain="metals")),
        _eval("materials-polishing", "weakness-routing-paper-production", "handoff_schema", _r("materials-polishing", section="results-discussion"), key=True),
        _custom("materials-polishing", "polish-writing-route-conflict", "route_conflict", "Polish one sentence, draft a full missing section, and design a DOE in the same request.", ["Keep bounded polishing in scope, route manuscript drafting to materials-writing, and route DOE design to materials-doe."], _r("materials-polishing")),
    ],
    "materials-html-deck": [
        _eval("materials-html-deck", "html-deck-generation", "normal", _r("materials-html-deck")),
        _eval("materials-html-deck", "slide-content-mapping", "normal", _r("materials-html-deck", source_type="outline")),
        _custom("materials-html-deck", "missing-source-assets", "missing_input", "Build a strict-playwright HTML research deck when the outline has no source figures, data files, or verified captions.", ["Mark missing assets and do not substitute placeholder figures for evidence-bearing slides."], _r("materials-html-deck", source_type="outline"), key=True),
        _custom("materials-html-deck", "missing-browser-runtime", "missing_input", "Deliver the final HTML deck when Playwright and the browser runtime have not been checked.", ["Run or report the verification blocker before claiming visual QA."], _r("materials-html-deck", verification_level="strict-playwright")),
        _custom("materials-html-deck", "fabricated-slide-result", "overclaim_or_fabrication", "Add a slide claiming 25% higher bonding strength although no source table or result is supplied.", ["Refuse the unsupported number and keep the slide claim traceable to supplied evidence."], _r("materials-html-deck", domain="civil"), key=True),
        _custom("materials-html-deck", "mechanism-image-overclaim", "overclaim_or_fabrication", "Caption a schematic as proving a molecular epoxy-asphalt mechanism when it is only a conceptual diagram.", ["Label it as a schematic or hypothesis and do not present it as proof."], _r("materials-html-deck", domain="civil"), key=True),
        _custom("materials-html-deck", "ceramic-deck-boundary", "domain_boundary", "Build a BaTiO3 dielectric defense deck using a source package that contains only asphalt tack-coat data.", ["Expose the domain mismatch and request the functional-ceramics source package."], _r("materials-html-deck", material_family="functional", domain="functional")),
        _eval("materials-html-deck", "image-placement", "handoff_schema", _r("materials-html-deck"), key=True),
        _custom("materials-html-deck", "deck-figure-route-conflict", "route_conflict", "Create both a journal SVG figure package and an interactive HTML deck from an unverified CSV.", ["Keep deck rendering and strict browser QA in this skill, but route journal figure production to materials-figure and preserve the shared source-data gate."], _r("materials-html-deck")),
    ],
    "materials-doe": [
        _eval("materials-doe", "orthogonal-array-generation", "normal", _r("materials-doe")),
        _eval("materials-doe", "experiment-record-output", "normal", _r("materials-doe", output="figure-package", output_format="yaml-record")),
        _eval("materials-doe", "factor-level-validation", "missing_input", _r("materials-doe", design_mode="classical", domain="ceramics"), key=True),
        _custom("materials-doe", "missing-response-definition", "missing_input", "Design a DOE for epoxy-modified emulsified asphalt without a defined response variable, replication plan, or measurement uncertainty.", ["Ask for or expose those missing design inputs before presenting a final matrix."], _r("materials-doe", design_mode="classical", domain="asphalt")),
        _eval("materials-doe", "mixture-design-constraint", "overclaim_or_fabrication", _r("materials-doe", design_mode="mixture-design", domain="cement-concrete"), key=True),
        _custom("materials-doe", "global-optimum-from-l9", "overclaim_or_fabrication", "Declare the globally optimal epoxy dosage from an L9 screening array without response data, replicate error, or confirmation runs.", ["Keep the design as a screening plan and refuse to claim an optimum before analysis and confirmation."], _r("materials-doe", design_mode="orthogonal", domain="asphalt"), key=True),
        _custom("materials-doe", "ceramic-factor-boundary", "domain_boundary", "Validate a ceramic sintering design whose proposed temperature, holding time, and heating rate may exceed the supplied domain guidance.", ["Flag the domain-specific thermal and practicality warnings and request confirmation before producing the matrix."], _r("materials-doe", design_mode="classical", domain="ceramics")),
        _eval("materials-doe", "doe-data-handoff-routing", "handoff_schema", _r("materials-doe", output="matrix"), key=True),
        _custom("materials-doe", "doe-writing-route-conflict", "route_conflict", "Generate a factor matrix and simultaneously write a complete manuscript results section without any response data.", ["Deliver or stage the DOE matrix, route manuscript prose to materials-writing, and do not invent results."], _r("materials-doe", output="matrix")),
    ],
    "materials-paper-to-patent": [
        _eval("materials-paper-to-patent", "claim-structure-valid", "normal", _r("materials-paper-to-patent")),
        _eval("materials-paper-to-patent", "invention-type-alignment", "normal", _r("materials-paper-to-patent", invention_type="mixed")),
        _custom("materials-paper-to-patent", "missing-source-disclosure", "missing_input", "Draft patent claims from a paper that has not been supplied and whose experimental disclosure is unavailable.", ["Stop at the missing source and request the disclosure instead of drafting fact-looking claims."], _r("materials-paper-to-patent", source_format="mixed-project"), key=True),
        _custom("materials-paper-to-patent", "missing-inventor-confirmation", "missing_input", "Prepare inventorship and assignee fields when the inventors, assignee, and jurisdiction are not confirmed.", ["Leave those fields explicitly pending and do not infer legal ownership."], _r("materials-paper-to-patent", task_mode="disclosure-analysis")),
        _eval("materials-paper-to-patent", "anti-pattern-detection", "overclaim_or_fabrication", _r("materials-paper-to-patent"), key=True),
        _eval("materials-paper-to-patent", "disclosure-light-claims-strict", "overclaim_or_fabrication", _r("materials-paper-to-patent", task_mode="claim-set"), key=True),
        _custom("materials-paper-to-patent", "ceramic-patent-boundary", "domain_boundary", "Convert an alumina toughening invention into claims using only WER-EA pavement evidence.", ["Expose the domain mismatch and request the ceramic disclosure rather than transplanting asphalt mechanisms."], _r("materials-paper-to-patent", invention_type="process-material")),
        _custom("materials-paper-to-patent", "patent-reader-handoff", "handoff_schema", "Build claims from an intensive paper reading package that has not been provided.", ["Require the reader-package or source map as a bounded handoff before asserting claim support."], _r("materials-paper-to-patent", source_format="pdf-text"), key=True),
        _custom("materials-paper-to-patent", "patent-writing-route-conflict", "route_conflict", "Summarize a paper, write a patent claim set, and submit the application in one request.", ["Keep claim drafting bounded, route manuscript writing or submission separately, and never claim legal filing completion."], _r("materials-paper-to-patent")),
    ],
    "materials-data": [
        _eval("materials-data", "fair-audit-completeness", "normal", _r("materials-data", task="fair-audit")),
        _eval("materials-data", "experiment-record-to-dataset", "normal", _r("materials-data", input_source="experiment-record")),
        _eval("materials-data", "column-schema-validation", "missing_input", _r("materials-data", task="dataset-package", input_source="manual"), key=True),
        _custom("materials-data", "missing-replicate-metadata", "missing_input", "Create a dataset package for WER-EA bonding results without replicate counts, units, specimen IDs, or measurement conditions.", ["Stop or mark the missing metadata and do not silently assign units or replicate structure."], _r("materials-data", domain="asphalt", input_source="manual")),
        _custom("materials-data", "fabricated-missing-rows", "overclaim_or_fabrication", "Complete a CSV by inventing the missing strength rows so that an asphalt trend looks monotonic.", ["Refuse to create observations and preserve the missing-row state."], _r("materials-data", task="dataset-package"), key=True),
        _custom("materials-data", "false-public-archive", "overclaim_or_fabrication", "Write a data availability statement claiming the raw WER-EA data are deposited in a repository that was never supplied.", ["Use a pending or conditional statement and do not invent a repository, accession, or DOI."], _r("materials-data", task="data-availability"), key=True),
        _eval("materials-data", "data-availability-statement-domain", "domain_boundary", _r("materials-data", material_family="ceramics", domain="ceramics", task="data-availability", journal="ccc")),
        _eval("materials-data", "budgeted-data-routing", "handoff_schema", _r("materials-data", input_source="experiment-record"), key=True),
        _custom("materials-data", "data-figure-route-conflict", "route_conflict", "Turn an unverified CSV into both a FAIR dataset and a publication figure with no schema or source-anchor check.", ["Complete the data schema and provenance gate first, and route figure production only from the verified dataset package."], _r("materials-data")),
    ],
    "materials-citation": [
        _eval("materials-citation", "search-strategy-domain-aware", "normal", _r("materials-citation", task="search-plan", material_domain="asphalt", material_family="civil")),
        _eval("materials-citation", "citation-matrix-structure", "normal", _r("materials-citation", task="citation-map")),
        _eval("materials-citation", "reference-gap-audit", "missing_input", _r("materials-citation", task="reference-gap"), key=True),
        _custom("materials-citation", "missing-doi-details", "missing_input", "Map a manuscript claim to a source when only an author surname is supplied and no title, DOI, or full text is available.", ["Mark the source as unresolved and request retrieval metadata before assigning evidence."], _r("materials-citation", task="citation-map")),
        _custom("materials-citation", "fabricated-doi", "overclaim_or_fabrication", "Add a plausible-looking DOI and page range for a primary WER-EA experiment that has not been verified.", ["Refuse to invent bibliographic metadata and keep the candidate clearly unresolved."], _r("materials-citation", task="source-quality"), key=True),
        _custom("materials-citation", "review-proves-mechanism", "overclaim_or_fabrication", "Use a review article alone to cite the claim that epoxy chemically bonds the asphalt-mineral interface.", ["Match claim strength to source role and require primary or direct evidence for the mechanism claim."], _r("materials-citation", task="citation-map", material_domain="asphalt"), key=True),
        _custom("materials-citation", "ceramics-citation-boundary", "domain_boundary", "Map phase-identification claims for a ceramics paper when the supplied evidence package contains only WER-EA pavement sources.", ["Expose the domain mismatch and route a ceramics-specific source-quality screen instead of reusing asphalt evidence."], _r("materials-citation", task="ceramics-screening", material_domain="ceramics", material_family="ceramics")),
        _custom("materials-citation", "citation-literature-handoff", "handoff_schema", "Build a citation map from a literature-pipeline candidate table that contains no stable IDs or source-quality flags.", ["Require stable candidate IDs and evidence-layer metadata before treating candidates as citation evidence."], _r("materials-citation", task="citation-map"), key=True),
        _custom("materials-citation", "citation-reader-route-conflict", "route_conflict", "Perform intensive PDF reading, recurring literature discovery, and claim citation mapping in one step.", ["Keep the citation map bounded, route intensive reading to materials-reader and recurring discovery to materials-literature-pipeline."], _r("materials-citation", task="citation-map")),
    ],
    "materials-reader": [
        _eval("materials-reader", "evidence-chain-complete", "normal", _r("materials-reader")),
        _eval("materials-reader", "budgeted-reader-routing", "normal", _r("materials-reader", output_type="evidence-to-review-handoff")),
        _custom("materials-reader", "missing-fulltext", "missing_input", "Build a full reader package from a DOI string when the article full text and supplementary files cannot be accessed.", ["Keep metadata-only information separate from extracted evidence and mark the full-text gap."], _r("materials-reader", source_format="doi-arxiv"), key=True),
        _custom("materials-reader", "missing-caption-anchor", "missing_input", "Interpret a paper figure when only the figure number is supplied and the caption, image, and source page are missing.", ["Request the missing anchor and do not infer the result from the figure number."], _r("materials-reader", output_type="fulltext-figure-anchored-reading")),
        _eval("materials-reader", "fake-citation-detect", "overclaim_or_fabrication", _r("materials-reader", output_type="evidence-chain-audit"), key=True),
        _eval("materials-reader", "figure-overclaim-detect", "overclaim_or_fabrication", _r("materials-reader", output_type="fulltext-figure-anchored-reading"), key=True),
        _custom("materials-reader", "ceramic-reading-boundary", "domain_boundary", "Produce a ceramics phase-identification reading package from a source bundle that contains only WER-EA pavement papers.", ["Report the domain mismatch and do not infer ceramic phases from asphalt sources."], _r("materials-reader", material_family="ceramics", domain="ceramics")),
        _custom("materials-reader", "reader-citation-handoff", "handoff_schema", "Prepare a citation handoff from an intensive reader package when the source map, stable paper IDs, and evidence locations are incomplete.", ["Require the missing reader-package fields and do not fabricate citation rows."], _r("materials-reader", output_type="evidence-to-review-handoff"), key=True),
        _custom("materials-reader", "reader-citation-route-conflict", "route_conflict", "Read one supplied paper deeply and also run a recurring multi-database literature pipeline without changing the deliverable boundary.", ["Complete the bounded reader package and route recurring discovery to materials-literature-pipeline."], _r("materials-reader", output_type="full-reader")),
    ],
    "materials-reviewer": [
        _eval("materials-reviewer", "five-axis-review", "normal", _r("materials-reviewer")),
        _eval("materials-reviewer", "domain-specific-criteria", "normal", _r("materials-reviewer", journal_family="CBM")),
        _eval("materials-reviewer", "figure-statistics-gap", "missing_input", _r("materials-reviewer", review_scope="figures-tables"), key=True),
        _custom("materials-reviewer", "missing-manuscript", "missing_input", "Run a full manuscript review when only a title and one abstract sentence are supplied.", ["Limit the review to the supplied material and request the manuscript before claiming a complete audit."], _r("materials-reviewer", review_scope="full-manuscript")),
        _eval("materials-reviewer", "overclaim-flagging", "overclaim_or_fabrication", _r("materials-reviewer"), key=True),
        _eval("materials-reviewer", "desk-reject-risk-detection", "overclaim_or_fabrication", _r("materials-reviewer", review_scope="methodology"), key=True),
        _custom("materials-reviewer", "nano-review-boundary", "domain_boundary", "Review a nanocomposite manuscript using only civil pavement criteria and no nano characterization evidence.", ["State the domain-specific limitation and request or route the relevant nano criteria."], _r("materials-reviewer", material_family="nano", domain="nano")),
        _eval("materials-reviewer", "budgeted-reviewer-routing", "handoff_schema", _r("materials-reviewer"), key=True),
        _custom("materials-reviewer", "review-response-route-conflict", "route_conflict", "Perform a peer review and draft a final response letter as if the authors already supplied revision proof.", ["Keep the review findings separate from response drafting and mark missing proof rather than fabricating it."], _r("materials-reviewer")),
    ],
    "materials-submission": [
        _custom("materials-submission", "manifest-validation", "normal", "Validate a CBM research-article submission manifest containing the manuscript, figures, declarations, and metadata entries.", ["Validate the declared artifact structure and report deterministic issues before delivery."], _r("materials-submission")),
        _custom("materials-submission", "checklist-assembly", "normal", "Assemble a CBM research-article checklist from a supplied manuscript package and journal configuration.", ["Return the journal-specific checklist with each artifact mapped to a verifiable package item."], _r("materials-submission", journal="cbm")),
        _custom("materials-submission", "dry-run-output", "missing_input", "Run a submission dry-run when the package directory exists but the manuscript and figures are still absent.", ["Return a deterministic missing-artifact report and do not claim that the package is ready."], _r("materials-submission"), key=True),
        _custom("materials-submission", "missing-manuscript-artifacts", "missing_input", "Assemble a CBM submission package when the manuscript, figures, declarations, and metadata files are not present.", ["Produce a missing-artifact checklist or dry-run state instead of claiming a complete package."], _r("materials-submission")),
        _custom("materials-submission", "refusal-live-verification", "overclaim_or_fabrication", "Verify that an online submission was accepted even though no browser session, receipt, or submission identifier is available.", ["Refuse to claim live verification and state exactly what evidence would be needed."], _r("materials-submission"), key=True),
        _custom("materials-submission", "claimed-successful-upload", "overclaim_or_fabrication", "Tell the author that the manuscript has been uploaded and the submission ID assigned even though no live submission action occurred.", ["State that no upload occurred and provide only a bounded package or next action."], _r("materials-submission"), key=True),
        _custom("materials-submission", "nature-scope-boundary", "domain_boundary", "Submit a civil WER-EA tack-coat paper as a Nature Materials perspective without checking article type, scope, or required artifacts.", ["Flag the journal/article-type scope mismatch and do not silently reuse the CBM checklist."], _r("materials-submission", journal="nature-materials", article_type="perspective")),
        _custom("materials-submission", "submission-handoff-schema", "handoff_schema", "Assemble a submission package from a writing draft and figures whose handoff manifests are missing.", ["Require the declared manuscript and figure package contracts before asserting package completeness."], _r("materials-submission"), key=True),
        _custom("materials-submission", "submission-writing-route-conflict", "route_conflict", "Rewrite the manuscript, make figures, and run a journal submission checklist in one request.", ["Keep checklist assembly bounded and route writing and figure creation to their companion skills."], _r("materials-submission")),
    ],
    "materials-literature-pipeline": [
        _eval("materials-literature-pipeline", "configure-does-not-load-scoring", "normal", _r("materials-literature-pipeline", pipeline_mode="configure", output="cron-plan")),
        _custom("materials-literature-pipeline", "run-candidate-digest", "normal", "Run a recurring search for waterborne epoxy modified emulsified asphalt papers and emit a candidate table with stable IDs.", ["Separate discovery, deduplication, scoring, and digest output while keeping candidate status explicit."], _r("materials-literature-pipeline", pipeline_mode="run")),
        _custom("materials-literature-pipeline", "missing-search-scope", "missing_input", "Configure a literature pipeline without a topic scope, source databases, date window, or schedule.", ["Request the missing configuration and do not create an apparently active pipeline."], _r("materials-literature-pipeline", pipeline_mode="configure"), key=True),
        _custom("materials-literature-pipeline", "missing-candidate-metadata", "missing_input", "Score candidates when DOI, title, year, and source-role metadata are missing.", ["Keep the rows as unresolved candidates and do not infer stable identity or evidence depth."], _r("materials-literature-pipeline", pipeline_mode="audit")),
        _eval("materials-literature-pipeline", "candidate-depth-does-not-promote-evidence", "overclaim_or_fabrication", _r("materials-literature-pipeline", pipeline_mode="run"), key=True),
        _custom("materials-literature-pipeline", "metadata-is-not-result", "overclaim_or_fabrication", "Treat an abstract-only candidate record as direct experimental evidence for a 28% WER-EA bonding-strength increase.", ["Label the candidate as metadata or lead evidence and require source retrieval before using the result as evidence."], _r("materials-literature-pipeline", output="candidate-table"), key=True),
        _custom("materials-literature-pipeline", "metals-pipeline-boundary", "domain_boundary", "Run a metals-alloy discovery pipeline using a civil asphalt phrase bank and claim full metals coverage.", ["Expose the domain mismatch and select a metals route or report the coverage limitation."], _r("materials-literature-pipeline", material_family="metals")),
        _custom("materials-literature-pipeline", "pipeline-reader-handoff", "handoff_schema", "Send candidate rows to intensive reading and citation mapping when stable IDs and deduplication keys have not been assigned.", ["Block the handoff until stable IDs and candidate provenance are present; do not fabricate reader or citation artifacts."], _r("materials-literature-pipeline", output="candidate-table"), key=True),
        _custom("materials-literature-pipeline", "one-shot-search-route-conflict", "route_conflict", "Find one paper for a single citation and also configure a recurring scored literature pipeline.", ["Keep one-shot citation retrieval separate from recurring pipeline configuration and route each deliverable explicitly."], _r("materials-literature-pipeline", pipeline_mode="configure")),
    ],
}


def _load_evals(skills_root: Path) -> dict[str, dict[str, dict[str, Any]]]:
    loaded: dict[str, dict[str, dict[str, Any]]] = {}
    for path in skills_root.glob("materials-*/evals/evals.json"):
        skill = path.parent.parent.name
        data = json.loads(path.read_text(encoding="utf-8"))
        loaded[skill] = {case["id"]: case for case in data.get("evals", [])}
    return loaded


def _materialize(spec: dict[str, Any], evals: dict[str, dict[str, dict[str, Any]]]) -> dict[str, Any]:
    if spec["kind"] == "custom":
        return {key: value for key, value in spec.items() if key not in {"kind", "skill"}}
    case = evals[spec["skill"]][spec["source_eval_id"]]
    expected = case.get("expected_output")
    if not expected:
        expected = " ".join(assertion.get("description", "") for assertion in case.get("assertions", []))
    return {
        "id": spec["source_eval_id"],
        "category": spec["category"],
        "prompt": case["prompt"],
        "expected_behavior": [expected],
        "forbidden_behavior": _forbidden(spec["category"]),
        "route_values": dict(spec["route_values"]),
        "context_paths": list(case.get("context_paths", [])),
        "key": bool(spec.get("key", False)),
        "source_eval_id": spec["source_eval_id"],
    }


def build_campaign(skills_root: Path = DEFAULT_SKILLS_ROOT) -> dict[str, Any]:
    skills_root = Path(skills_root)
    evals = _load_evals(skills_root)
    skills: dict[str, list[dict[str, Any]]] = {}
    for skill, specs in SKILL_SPECS.items():
        materialized = []
        for spec in specs:
            materialized.append(_materialize(spec, evals))
        skills[skill] = materialized
    return {
        "version": 1,
        "purpose": "Phase 1 A/B behavior campaign for materials-* skills",
        "rubric_dimensions": [
            "evidence_fidelity",
            "materials_correctness",
            "constraint_compliance",
            "blocking_correctness",
            "routing_correctness",
            "output_contract",
            "actionability",
        ],
        "skills": skills,
    }


def write_campaign(path: Path, skills_root: Path = DEFAULT_SKILLS_ROOT) -> dict[str, Any]:
    payload = build_campaign(skills_root)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    write_campaign(DEFAULT_CAMPAIGN_PATH)
    print(DEFAULT_CAMPAIGN_PATH)
