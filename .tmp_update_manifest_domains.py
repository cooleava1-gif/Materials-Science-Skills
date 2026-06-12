#!/usr/bin/env python3
"""Update manifests for ceramics + thermal-insulation domains."""
import os

BASE = r"C:\Users\97218\Desktop\civil-materials-skills-release"

# 1. research
path = os.path.join(BASE, "skills/materials-research/manifest.yaml")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Domain axis: add ceramics + thermal-insulation
old = "      sustainability-durability:\n        path: static/fragments/domain/sustainability-durability.md\n        triggers: [\"sustainability\", \"durability\", \"life cycle\", \"LCA\", \"carbon\", \"sustainable\", \"\u53ef\u6301\", \"\u8010\u4e45\"]"
new = old + "\n" + """\
      ceramics:
        path: static/fragments/domain/ceramics.md
        triggers: ["ceramic", "ceramics", "sintering", "alumina", "zirconia", "silicon carbide", "nitride", "\u9676\u74f7", "\u70e7\u7ed3"]
      thermal-insulation:
        path: static/fragments/domain/thermal-insulation.md
        triggers: ["thermal insulation", "insulation", "aerogel", "foam", "thermal conductivity", "building envelope", "\u9694\u70ed", "\u4fdd\u6e29", "\u6c14\u51dd\u80f6"]"""
content = content.replace(old, new, 1)

# Journal axis: add new journals
old = "      generic:\n        path: static/fragments/journal/generic.md\n        triggers: [\"journal\", \"submission\", \"SCI\", \"general\"]"
new = old + "\n" + """\
      jacers:
        path: static/fragments/journal/jacers.md
        triggers: ["JACerS", "Journal of the American Ceramic Society", "American Ceramic Society"]
      ceramics-international:
        path: static/fragments/journal/ceramics-international.md
        triggers: ["Ceramics International", "ceram. int.", "ceramics international"]
      energy-buildings:
        path: static/fragments/journal/energy-buildings.md
        triggers: ["Energy and Buildings", "energy build.", "energy buildings"]
      building-environment:
        path: static/fragments/journal/building-environment.md
        triggers: ["Building and Environment", "build. environ.", "building environment"]"""
content = content.replace(old, new, 1)

# on_demand: add journal format refs
old = "      path: ../_shared/journal-formats/jbe.md\n      when: \"The target journal is JBE, Journal of Building Engineering.\""
new = old + "\n" + """\
    journal-jacers-facts:
      path: ../_shared/journal-formats/jacers.md
      when: "The target journal is JACerS."
    journal-ceramics-international-facts:
      path: ../_shared/journal-formats/ceramics-international.md
      when: "The target journal is Ceramics International."
    journal-energy-buildings-facts:
      path: ../_shared/journal-formats/energy-buildings.md
      when: "The target journal is Energy and Buildings."
    journal-building-environment-facts:
      path: ../_shared/journal-formats/building-environment.md
      when: "The target journal is Building and Environment.""""
content = content.replace(old, new, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("  UPDATED research")

# 2. citation
path = os.path.join(BASE, "skills/materials-citation/manifest.yaml")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
old = "      civil-materials:\n        path: static/fragments/domain/materials.md\n        triggers: [\"civil materials\", \"construction materials\", \"\u571f\u6728\u6750\u6599\", \"\u5efa\u7b51\u6750\u6599\"]"
new = old + "\n" + """\
      ceramics:
        path: static/fragments/domain/ceramics.md
        triggers: ["ceramic", "sintering", "alumina", "zirconia", "carbide", "nitride", "\u9676\u74f7"]
      thermal-insulation:
        path: static/fragments/domain/thermal-insulation.md
        triggers: ["thermal insulation", "aerogel", "foam", "insulation", "thermal conductivity", "\u9694\u70ed", "\u4fdd\u6e29"]"""
content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("  UPDATED citation")

# 3. data
path = os.path.join(BASE, "skills/materials-data/manifest.yaml")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
old = "      civil-materials:\n        path: static/fragments/domain/materials.md\n        triggers: [\"civil materials\", \"construction materials\", \"durability\", \"sustainability\"]"
new = old + "\n" + """\
      ceramics:
        path: static/fragments/domain/ceramics.md
        triggers: ["ceramic", "sintering", "alumina", "zirconia", "\u9676\u74f7"]
      thermal-insulation:
        path: static/fragments/domain/thermal-insulation.md
        triggers: ["thermal insulation", "aerogel", "foam", "insulation", "\u9694\u70ed", "\u4fdd\u6e29"]"""
content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("  UPDATED data")

# 4. figure
path = os.path.join(BASE, "skills/materials-figure/manifest.yaml")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
old = "      civil-materials:\n        path: references/summary-figures.md\n        triggers: [\"civil materials\", \"construction materials\", \"\u571f\u6728\u6750\u6599\", \"\u5efa\u7b51\u6750\u6599\"]"
new = old + "\n" + """\
      ceramics:
        path: static/fragments/domain/ceramics.md
        triggers: ["ceramic", "sintering", "microstructure", "alumina", "zirconia", "\u9676\u74f7"]
      thermal-insulation:
        path: static/fragments/domain/thermal-insulation.md
        triggers: ["thermal insulation", "aerogel", "foam", "porous", "\u9694\u70ed", "\u4fdd\u6e29"]"""
content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("  UPDATED figure")

# 5. reviewer
path = os.path.join(BASE, "skills/materials-reviewer/manifest.yaml")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
old = "      mechanism:\n        path: references/mechanism-evidence-checklist.md\n        triggers: [\"mechanism\", \"FTIR\", \"SEM\", \"fluorescence\", \"rheology\", \"XRD\", \"TG\"]"
new = old + "\n" + """\
      ceramics:
        path: references/materials-criteria.md
        triggers: ["ceramic", "sintering", "alumina", "zirconia", "carbide", "\u9676\u74f7"]
      thermal-insulation:
        path: references/materials-criteria.md
        triggers: ["thermal insulation", "aerogel", "foam", "insulation", "\u9694\u70ed", "\u4fdd\u6e29"]"""
content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("  UPDATED reviewer")

print("\nDone")
