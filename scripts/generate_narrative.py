#!/usr/bin/env python3
"""Generate a materials science narrative guide from a Material Registry entry.

Usage:
    python scripts/generate_narrative.py --material-id asphalt-pavement
    python scripts/generate_narrative.py --material-id cement-concrete --output my-guide.md
    python scripts/generate_narrative.py --all                # generate all supported
    python scripts/generate_narrative.py --all --upgrade      # also generate for skeleton-tier
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = REPO_ROOT / "_shared" / "material-registry"
ENTRIES_DIR = REGISTRY_DIR / "entries"
TEMPLATE_FILE = REGISTRY_DIR / "narrative-template.md"
OUTPUT_DIR = REPO_ROOT / "skills" / "materials-writing" / "references"

# ── Material-specific narrative data ──────────────────────────────────────
# These override or fill in details that can't be derived from the registry alone.
# Each entry supplements what the template + registry produce.

NARRATIVE_OVERRIDES: dict[str, dict[str, Any]] = {
    "asphalt-pavement": {
        "material_context": "asphalt emulsion and pavement materials",
        "problem_statement": "Asphalt pavements dominate road infrastructure, but conventional binders suffer from moisture damage, aging, or inadequate bonding at interfaces",
        "solution_limitation": "Polymer modification or additive approaches improve performance but often sacrifice workability, storage stability, or cost-effectiveness",
        "specific_gap": "specific gap: e.g., moisture-resistant tack coat, long-term aging resistance, low-temperature cracking",
        "approach": "approach: waterborne epoxy modification, nano-additive, bio-based rejuvenator",
        "key_finding": "key finding: e.g., 30% improvement in moisture-conditioned bonding",
        "competing_requirement": "competing requirement: sprayability, storage stability, cost",
        "application_target": "field application, specification development, or lifecycle improvement",
        "tradeoff": "performance-processability trade-off",
        "evidence_chain": [
            "Modification → emulsion properties (particle size, viscosity, stability) → film formation → bonding/mechanical performance → durability.",
            "Each modification variable should link to a microstructural or chemical feature before connecting to performance.",
            "Mechanism claims require FTIR, SEM, or thermal analysis as complementary evidence.",
        ],
        "intro_structure": "road infrastructure context → moisture/aging damage mechanism → current solutions and limitations → specific gap → approach → roadmap",
        "methods_structure": "materials (asphalt grade, emulsifier, modifier) → emulsion preparation → test methods (bonding, rheology, durability) → standards",
        "results_structure": "emulsion characterization → bonding performance → dosage optimization → durability → mechanism evidence",
        "discussion_structure": "connect results back to modification mechanism → performance improvement → comparison with literature → practical implications",
        "conclusions_structure": "concise findings without overclaim; note limitations (lab vs field) and future work",
        "keywords": "tack coat, interlayer bonding, moisture damage, stripping, adhesion, cohesion, waterborne epoxy, emulsified asphalt, modified asphalt, storage stability, viscosity, particle size distribution, FTIR, SEM, TG-DSC, aging, freeze-thaw, pull-off strength, shear strength",
        "reviewer_safe_language": [
            '"The increase in bond strength may be attributed to epoxy crosslinking at the interface" (not "is caused by").',
            '"FTIR suggests the formation of C-O-C ether bonds" (not "confirms the curing mechanism").',
            '"The moisture-conditioned retention ratio of X% indicates improved resistance compared to the control" (not "proves moisture resistance").',
            '"The optimum epoxy content of 10-15% was identified under laboratory conditions" (not "the optimal dosage for field application").',
        ],
    },
    "cement-concrete": {
        "material_context": "cement and concrete",
        "problem_statement": "Concrete is the most widely used construction material, but its durability, carbon footprint, or mechanical performance under extreme conditions remains a challenge",
        "solution_limitation": "Supplementary cementitious materials or novel additives can improve specific properties but often introduce trade-offs in workability, setting time, or early strength",
        "specific_gap": "specific gap: e.g., chloride resistance, high-early-strength, low-carbon binder",
        "approach": "approach: ternary blend, nano-silica, geopolymer activation",
        "key_finding": "key finding: e.g., 40% reduction in chloride diffusion",
        "competing_requirement": "competing requirement: 28-day strength, workability, cost",
        "application_target": "structural application, specification revision, or carbon reduction",
        "tradeoff": "durability-sustainability trade-off",
        "evidence_chain": [
            "Mix design → fresh properties → hydration → microstructure → mechanical/durability properties.",
            "Each SCM or additive should link to hydration products (XRD, TG-DSC, SEM) before connecting to macro-properties.",
            "Durability claims require at least two complementary tests (e.g., chloride penetration + carbonation).",
        ],
        "intro_structure": "construction demand → durability challenge → current solutions and limitations → specific gap → approach → roadmap",
        "methods_structure": "materials (cement type, SCMs, aggregates, admixtures) → mix design → curing → testing methods and standards",
        "results_structure": "fresh properties → strength development → microstructure → durability → comparison with literature",
        "discussion_structure": "connect results back to hydration mechanism → microstructure-property relationship → practical implications → limitations",
        "conclusions_structure": "concise findings without overclaim; note limitations (lab specimens vs structural elements) and future work",
        "keywords": "supplementary cementitious materials, fly ash, silica fume, ground granulated blast-furnace slag, geopolymer, alkali-activated, chloride penetration, carbonation, freeze-thaw resistance, hydration, C-S-H, portlandite, ettringite, water-binder ratio, compressive strength, elastic modulus, durability, service life",
        "reviewer_safe_language": [
            '"The reduction in chloride diffusion coefficient may be attributed to pore refinement by silica fume" (not "is caused by pore refinement").',
            '"XRD indicates the consumption of portlandite and formation of additional C-S-H" (not "proves the pozzolanic reaction").',
            '"The 28-day compressive strength of X MPa meets the design requirement of Y MPa" (not "the concrete is strong enough").',
            '"The ternary blend shows promise for marine exposure applications" (not "is suitable for marine structures").',
        ],
    },
    "structural-ceramics": {
        "material_context": "structural and advanced ceramics",
        "problem_statement": "Ceramics offer high-temperature stability, wear resistance, or functional properties that metals and polymers cannot match",
        "solution_limitation": "However, their engineering adoption is limited by brittleness, processing cost, or difficulty in fabricating complex shapes",
        "specific_gap": "specific gap: e.g., sintering temperature reduction, toughness improvement, conductivity enhancement",
        "approach": "approach: composition design, processing optimization, additive",
        "key_finding": "key finding",
        "competing_requirement": "competing requirement: density, hardness, phase purity",
        "application_target": "application",
        "tradeoff": "processing-property trade-off",
        "evidence_chain": [
            "Processing → density/porosity → mechanical/thermal properties → application relevance.",
            "Each processing variable should link to a microstructural feature before connecting to properties.",
            "Mechanism claims require at least two complementary characterization techniques.",
        ],
        "intro_structure": "application context → material limitations → specific gap → approach → roadmap",
        "methods_structure": "powder → forming → sintering → characterization → testing standards",
        "results_structure": "density → phase → microstructure → mechanical → thermal/functional (in logical dependency order)",
        "discussion_structure": "connect results back to processing → structure → property chain; compare with literature; identify trade-offs",
        "conclusions_structure": "concise findings without overclaim; note limitations and future work",
        "keywords": "sintering, densification, grain growth, phase transformation, grain boundary, Weibull modulus, R-curve, thermal shock, solid solution, second phase, intergranular, transgranular, fracture mirror, flaw population",
        "reviewer_safe_language": [
            '"The increase in flexural strength may be attributed to reduced porosity" (not "caused by").',
            '"XRD suggests the presence of" (not "confirms" unless Rietveld with good fit).',
            '"The Weibull modulus of m = X indicates relatively low variability for a ceramic processed by Y" (not "high reliability").',
        ],
    },
    "thermal-insulation": {
        "material_context": "thermal insulation materials",
        "problem_statement": "Building energy consumption accounts for a large share of total energy use, and thermal insulation is the most direct strategy for reducing heating and cooling demand",
        "solution_limitation": "Current insulation materials face a trade-off between thermal performance and mechanical integrity, or between low conductivity and moisture durability",
        "specific_gap": "specific gap: mechanical/thermal/moisture trade-off",
        "approach": "approach: aerogel, foam, VIP, PCM composite design",
        "key_finding": "key finding: optimum formulation balancing thermal, mechanical, and durability performance",
        "competing_requirement": "competing requirement: thermal conductivity, mechanical strength, moisture resistance",
        "application_target": "building insulation application scenario",
        "tradeoff": "thermal-mechanical-durability trade-off",
        "evidence_chain": [
            "Formulation → pore structure → thermal conductivity → mechanical strength → durability → application suitability.",
            "Each application claim must be supported by the appropriate service-condition test.",
            "Moisture effect must be quantified before building application can be claimed.",
        ],
        "intro_structure": "energy context → insulation limits → specific gap (mechanical/thermal/moisture trade-off) → approach",
        "methods_structure": "raw materials → fabrication → density/porosity characterization → thermal measurement (standard, T_mean) → mechanical → durability",
        "results_structure": "first porosity/pore structure, then thermal, then mechanical, then durability (if any)",
        "discussion_structure": "benchmark against commercial insulation materials; discuss trade-offs; identify application window",
        "conclusions_structure": "report lambda value with test T_mean; note moisture sensitivity if present",
        "keywords": "thermal conductivity, lambda, R-value, U-value, ASTM C518, guarded hot plate, heat flow meter, mean temperature, thermal bridge, aerogel, xerogel, cryogel, VIP, fumed silica, MF, PU, phenolic foam, mineral wool, glass wool, EPS, XPS, vacuum insulation panel, phase change material, PCM, hygrothermal, moisture uptake",
        "reviewer_safe_language": [
            '"The thermal conductivity was 0.028 W/(m.K) at a mean temperature of 25 °C" (always report temperature).',
            '"The material shows promise for building insulation applications, pending verification of long-term hygrothermal performance."',
            '"Compared to commercial silica aerogel (lambda ~0.015), our material offers improved mechanical strength at the cost of higher conductivity (0.028 vs 0.015)."',
            'Do not claim "superinsulating" unless lambda < 0.020 W/(m.K) at relevant conditions.',
        ],
    },
    "thermoplastics": {
        "material_context": "thermoplastic polymers",
        "problem_statement": "Thermoplastics offer versatility in processing, recyclability, and a wide range of mechanical properties for diverse applications",
        "solution_limitation": "However, their performance is limited by temperature sensitivity (Tg, Tm), creep, and environmental stress cracking in demanding service conditions",
        "specific_gap": "specific gap: e.g., mechanical reinforcement, thermal stability enhancement, crystallization control",
        "approach": "approach: filler/blend/comonomer modification, annealing optimization",
        "key_finding": "key finding: improved property balance",
        "competing_requirement": "competing requirement: processability, cost, toughness",
        "application_target": "lightweight structural or functional application",
        "tradeoff": "stiffness-toughness or processability-performance trade-off",
        "evidence_chain": [
            "Polymer structure/processing → morphology (crystallinity, phase separation) → mechanical/thermal properties → application performance.",
            "Each processing or composition change should link to a morphological or structural feature.",
            "Thermal analysis (DSC, TGA) is essential for supporting thermal stability and crystallinity claims.",
        ],
        "intro_structure": "application context → polymer class and value → current limitations → specific gap → approach → roadmap",
        "methods_structure": "materials → processing (compounding, molding, annealing) → characterization (thermal, mechanical, morphological) → standards",
        "results_structure": "thermal transitions → morphology → mechanical properties → correlation with structure",
        "discussion_structure": "connect structure to properties → compare with neat polymer and literature → identify trade-offs and mechanisms",
        "conclusions_structure": "concise findings; note processing limitations and application boundaries",
        "keywords": "thermoplastic, melt processing, injection molding, extrusion, crystallinity, glass transition, melting temperature, DSC, TGA, DMA, tensile strength, Young's modulus, elongation at break, impact strength, creep resistance",
        "reviewer_safe_language": [
            '"The increase in crystallinity may contribute to the observed stiffness improvement" (not "causes").',
            '"DSC indicates a Tg shift of X °C, suggesting restricted chain mobility" (not "proves").',
            '"The material exhibits potential for automotive interior applications pending creep and aging validation."',
        ],
    },
    "thermosets": {
        "material_context": "thermosetting polymers",
        "problem_statement": "Thermosetting polymers offer superior thermal stability, chemical resistance, and mechanical integrity compared to thermoplastics",
        "solution_limitation": "However, their brittleness, irreversible curing, and difficulty in recycling limit broader adoption, especially in large-scale applications",
        "specific_gap": "specific gap: e.g., toughness improvement, curing cycle optimization, bio-based thermoset development",
        "approach": "approach: formulation design, curing agent selection, nano-filler toughening",
        "key_finding": "key finding: improved thermomechanical balance",
        "competing_requirement": "competing requirement: Tg, crosslink density, processability",
        "application_target": "high-performance adhesive, coating, or composite application",
        "tradeoff": "toughness-stiffness or reactivity-performance trade-off",
        "evidence_chain": [
            "Resin/hardener chemistry → curing kinetics → crosslinked network → thermomechanical properties → performance.",
            "Curing characterization (DSC, rheology) is essential for understanding the structure-property relationship.",
            "Tg alone is insufficient to prove network structure — crosslink density from DMA should be reported.",
        ],
        "intro_structure": "application context → limitations of current thermosets → specific gap → formulation/processing approach → roadmap",
        "methods_structure": "materials → formulation → curing schedule → characterization (DSC, DMA, TGA, mechanical) → standards",
        "results_structure": "curing behavior → network characterization → thermal/mechanical properties → structure-property correlation",
        "discussion_structure": "connect curing chemistry to network structure to macro-properties; compare with baseline formulation",
        "conclusions_structure": "concise findings; note curing constraints and long-term performance unknowns",
        "keywords": "epoxy resin, phenolic, polyimide, curing kinetics, crosslink density, glass transition temperature, DMA, DSC, TGA, FTIR, pot life, gel time, post-cure, thermoset, thermomechanical, flexural modulus, adhesive strength",
        "reviewer_safe_language": [
            '"DMA suggests a crosslink density of X mol/cm³ based on the rubbery plateau modulus" (not "confirms").',
            '"The Tg increased from X to Y °C, indicating a more densely crosslinked network" (not "proving").',
            '"The formulation shows promise for structural adhesive applications pending long-term aging and creep data."',
        ],
    },
    "rubber-elastomers": {
        "material_context": "rubber and elastomer materials",
        "problem_statement": "Elastomers are essential for sealing, vibration isolation, and flexible component applications due to their high elastic recovery",
        "solution_limitation": "However, their performance degrades under heat, ozone, and oil exposure, and filler reinforcement optimization remains a challenge",
        "specific_gap": "specific gap: e.g., aging resistance, rolling resistance reduction, oil resistance improvement",
        "approach": "approach: filler system optimization, blend formulation, curing system design",
        "key_finding": "key finding: improved durability-performance balance",
        "competing_requirement": "competing requirement: elasticity, hardness, processability",
        "application_target": "tire, seal, or vibration isolation application",
        "tradeoff": "elasticity-damping or durability-processability trade-off",
        "evidence_chain": [
            "Formulation → curing → crosslink network → mechanical/dynamic properties → aging resistance.",
            "Filler dispersion characterization (SEM, rheology) is critical for understanding reinforcement.",
            "Aging claims require at least two aging conditions with property retention data.",
        ],
        "intro_structure": "application context → elastomer types → current limitations → specific gap → formulation/processing approach → roadmap",
        "methods_structure": "materials → compounding → curing → characterization (mechanical, dynamic, aging) → standards",
        "results_structure": "curing characteristics → mechanical properties → dynamic properties → aging resistance → structure-property correlation",
        "discussion_structure": "connect formulation to crosslink network to performance; compare with unfilled baseline; discuss filler dispersion effects",
        "conclusions_structure": "concise findings; note aging test limitations and application-specific validation needs",
        "keywords": "natural rubber, SBR, EPDM, silicone, polyurethane, vulcanization, crosslink density, DMA, tan delta, compression set, tear resistance, abrasion resistance, heat build-up, aging, ozone resistance, oil resistance, carbon black, silica, silane coupling agent",
        "reviewer_safe_language": [
            '"The reduction in compression set may be attributed to a higher crosslink density" (not "caused by").',
            '"DMA tan delta peak temperature suggests improved wet skid resistance" (not "proves").',
            '"The compound shows potential for dynamic applications pending fatigue test validation."',
        ],
    },
    "polymer-composites": {
        "material_context": "fiber-reinforced polymer composites",
        "problem_statement": "Fiber-reinforced polymer composites offer exceptional specific strength and stiffness for lightweight structural applications",
        "solution_limitation": "However, their adoption is limited by manufacturing cost, out-of-plane weakness, joining complexity, and environmental durability concerns",
        "specific_gap": "specific gap: e.g., interfacial bonding improvement, fatigue performance, manufacturing efficiency, recyclability",
        "approach": "approach: fiber/matrix interface optimization, hybridization, manufacturing process modification",
        "key_finding": "key finding: improved structural efficiency",
        "competing_requirement": "competing requirement: strength, stiffness, toughness, cost",
        "application_target": "aerospace, automotive, or infrastructure structural application",
        "tradeoff": "performance-cost or strength-toughness trade-off",
        "evidence_chain": [
            "Fiber/matrix selection → processing → interface quality → laminate properties → structural performance.",
            "Interface characterization (SEM, ILSS, micro-droplet) is critical for understanding load transfer.",
            "Environmental durability claims require conditioned testing (moisture, temperature, UV).",
        ],
        "intro_structure": "lightweight demand → composite types → current limitations → specific gap → approach → roadmap",
        "methods_structure": "materials (fiber, matrix) → laminate design → manufacturing → specimen preparation → testing standards",
        "results_structure": "laminate quality → mechanical properties (tension, flexure, ILSS) → fracture analysis → conditioned properties",
        "discussion_structure": "connect processing to interface quality to mechanical performance; compare with literature; discuss failure modes",
        "conclusions_structure": "concise findings; note manufacturing scale-up and long-term durability as limitations",
        "keywords": "CFRP, GFRP, AFRP, carbon fiber, glass fiber, aramid, epoxy matrix, laminate, fiber volume fraction, lay-up, vacuum infusion, autoclave, interlaminar shear strength, ILSS, flexural strength, fatigue, impact, fracture toughness, delamination, interface, fiber bridging, moisture absorption",
        "reviewer_safe_language": [
            '"SEM suggests improved fiber-matrix adhesion" (not "proves perfect interface").',
            '"The ILSS increase may be attributed to better interfacial load transfer" (not "confirmed").',
            '"The laminate demonstrates potential for secondary structural applications pending fatigue and environmental validation."',
        ],
    },
    "ferrous-alloys": {
        "material_context": "ferrous alloys and steels",
        "problem_statement": "Steels remain the most widely used structural alloys due to their excellent strength-toughness balance and low cost",
        "solution_limitation": "However, their performance is limited by corrosion, hydrogen embrittlement, and the strength-ductility trade-off in demanding applications",
        "specific_gap": "specific gap: e.g., strength-ductility synergy, corrosion resistance, weldability improvement",
        "approach": "approach: microalloying, thermomechanical processing, heat treatment optimization",
        "key_finding": "key finding: improved mechanical balance or corrosion resistance",
        "competing_requirement": "competing requirement: strength, ductility, toughness, weldability, cost",
        "application_target": "structural, automotive, or energy-sector application",
        "tradeoff": "strength-ductility or strength-corrosion resistance trade-off",
        "evidence_chain": [
            "Composition/processing → microstructure (grain size, phase fraction, precipitates) → mechanical properties → application performance.",
            "Microstructure characterization (OM, SEM, EBSD, TEM) is essential for mechanism claims.",
            "Corrosion and environmental degradation claims require standardized testing with appropriate exposure conditions.",
        ],
        "intro_structure": "application context → alloy class → current limitations → specific gap → approach → roadmap",
        "methods_structure": "materials → processing (casting, rolling, heat treatment) → specimen preparation → characterization (OM, SEM, XRD, mechanical testing) → standards",
        "results_structure": "microstructure → mechanical properties → fracture analysis → environmental performance (if applicable)",
        "discussion_structure": "connect processing to microstructure to properties; compare with standard grades; discuss structure-property relationships",
        "conclusions_structure": "concise findings; note processing scalability limitations and application-specific considerations",
        "keywords": "ferrous alloy, carbon steel, alloy steel, stainless steel, martensite, ferrite, austenite, pearlite, bainite, tempering, quenching, annealing, precipitation hardening, grain refinement, inclusion, fatigue, fracture, corrosion, hydrogen embrittlement, EBSD, TEM, SEM, XRD, hardness, tensile, Charpy impact",
        "reviewer_safe_language": [
            '"Grain refinement from X to Y µm contributed to the observed strength increase via Hall-Petch strengthening" (not "caused by").',
            '"EBSD suggests a higher fraction of high-angle grain boundaries, which may improve toughness" (not "proves").',
            '"The alloy demonstrates potential for pipeline applications pending HIC and SSC testing."',
        ],
    },
}



def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _get_registry_entry(material_id: str) -> dict[str, Any]:
    path = ENTRIES_DIR / f"{material_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Registry entry not found: {material_id}.yaml")
    return _load_yaml(path)


def _get_archetype_figure_scripts(entry: dict[str, Any]) -> list[str]:
    """Extract figure scripts that exist for this material."""
    scripts = []
    for arch in entry.get("figure_archetypes", []) or []:
        if isinstance(arch, dict) and arch.get("figure_script"):
            scripts.append(arch["figure_script"])
    return scripts


def _format_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def generate_narrative(material_id: str) -> str:
    """Generate a narrative guide for a material system."""
    entry = _get_registry_entry(material_id)
    overrides = NARRATIVE_OVERRIDES.get(material_id, {})

    # Fallback: derive what we can from the registry
    if not overrides:
        desc = entry.get("description", {})
        summary = desc.get("summary", material_id)
        problems = desc.get("engineering_problems", [])
        char_methods = [c.get("method", "") for c in entry.get("characterization", []) or [] if isinstance(c, dict)]
        figure_count = len(entry.get("figure_archetypes", []) or [])

        overrides = {
            "material_context": summary,
            "problem_statement": problems[0] if problems else f"The engineering challenge of {summary}",
            "solution_limitation": problems[1] if len(problems) > 1 else "requires systematic investigation to establish structure-property relationships",
            "specific_gap": "specific gap in current understanding or performance",
            "approach": "material design and characterization approach",
            "key_finding": "key evidence",
            "competing_requirement": "competing design requirements",
            "application_target": "relevant application",
            "tradeoff": "performance trade-off",
            "evidence_chain": [
                f"Processing → structure → properties → performance relationships must be systematically established for {summary}.",
                "Each claim should be supported by at least one characterization technique.",
                "Mechanism claims require complementary characterization evidence.",
            ],
            "intro_structure": "application context → material class → current limitations → specific gap → approach → roadmap",
            "methods_structure": "materials → synthesis/fabrication → characterization → testing → standards",
            "results_structure": "follow the logical chain from basic properties to application-relevant performance",
            "discussion_structure": "connect results to structure-property relationships; compare with literature; identify trade-offs and limitations",
            "conclusions_structure": "concise findings; note limitations and future work",
            "keywords": ", ".join(char_methods + [f"{prop.get('name', '')}" for prop in entry.get("properties", []) or [] if isinstance(prop, dict)]),
            "reviewer_safe_language": [
                '"The observed change may be attributed to" (not "is caused by").',
                '"The characterization data suggests" (not "proves" or "confirms").',
                '"The material shows potential for [application] pending further validation under service conditions."',
            ],
        }

    # Build the narrative markdown
    lines = []
    lines.append(f"# {entry.get('name', material_id)} Narrative")
    lines.append("")
    lines.append(f"For {overrides['material_context']}, the strongest manuscript narrative arc is usually:")
    lines.append("")
    lines.append(f"1. {overrides['problem_statement']},")
    lines.append(f"2. {overrides['solution_limitation']},")
    lines.append(f"3. this paper addresses **{overrides['specific_gap']}** through {overrides['approach']},")
    lines.append(f"4. we demonstrate that {overrides['key_finding']} while maintaining {overrides['competing_requirement']},")
    lines.append(f"5. the results suggest a pathway toward {overrides['application_target']} by resolving the {overrides['tradeoff']}.")
    lines.append("")
    lines.append("## Key evidence chain")
    lines.append("")
    lines.append(_format_list(overrides["evidence_chain"]))
    lines.append("")
    lines.append("## Common section structure")
    lines.append("")
    lines.append(f"- **Introduction**: {overrides['intro_structure']}")
    lines.append(f"- **Methods**: {overrides['methods_structure']}")
    lines.append(f"- **Results**: {overrides['results_structure']}")
    lines.append(f"- **Discussion**: {overrides['discussion_structure']}")
    lines.append(f"- **Conclusions**: {overrides['conclusions_structure']}")
    lines.append("")
    lines.append("## Useful keywords")
    lines.append("")
    lines.append(overrides["keywords"])
    lines.append("")
    lines.append("## Reviewer-safe language")
    lines.append("")
    lines.append(_format_list(overrides["reviewer_safe_language"]))
    lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--material-id", help="Registry material id (e.g., 'asphalt-pavement')")
    parser.add_argument("--output", help="Output file path (default: skills/materials-writing/references/<id>-narrative.md)")
    parser.add_argument("--all", action="store_true", help="Generate for all non-generic materials")
    parser.add_argument("--upgrade", action="store_true", help="Include skeleton-tier materials (upgrade to partial)")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout instead of file")
    parser.add_argument("--json", action="store_true", help="JSON summary output")
    args = parser.parse_args(argv)

    if args.material_id:
        targets = [args.material_id]
    elif args.all:
        # Collect all registry entries
        ids = []
        for path in sorted(ENTRIES_DIR.glob("*.yaml")):
            entry = _load_yaml(path)
            tier = entry.get("coverage_tier", "")
            if tier == "generic":
                continue
            if tier == "skeleton" and not args.upgrade:
                continue
            ids.append(entry.get("id", path.stem))
        targets = ids
    else:
        parser.print_help()
        return 1

    generated: list[dict[str, str]] = []
    errors: list[str] = []

    for mid in targets:
        try:
            text = generate_narrative(mid)
            entry = _get_registry_entry(mid)

            if args.stdout:
                print(f"--- {mid} ---")
                print(text)
            else:
                output_path = args.output or str(OUTPUT_DIR / f"{mid}-narrative.md")
                if not args.output:
                    # Default: overwrite existing narrative guides, create new ones
                    output_path = str(OUTPUT_DIR / f"{mid}-narrative.md")
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(text, encoding="utf-8")
                print(f"Generated: {output_file.as_posix()}")

            generated.append({"id": mid, "name": entry.get("name", mid)})
        except Exception as exc:
            errors.append(f"{mid}: {exc}")
            print(f"Error: {mid}: {exc}", file=sys.stderr)

    if args.json:
        print(json.dumps({
            "generated": len(generated),
            "errors": errors,
            "ids": [g["id"] for g in generated],
        }, indent=2, ensure_ascii=False))

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
