# {{material_name}} Narrative
{% if material_context %}
For {{material_context}}, the strongest manuscript narrative arc is usually:
{% else %}
The strongest manuscript narrative arc is usually:
{% endif %}

1. {{problem_statement}}
2. {{solution_limitation}}
3. this paper addresses **{{specific_gap}}** through {{approach}},
4. we demonstrate that {{key_finding}} while maintaining {{competing_requirement}},
5. the results suggest a pathway toward {{application_target}} by resolving the {{tradeoff}}.

## Key evidence chain

{% for item in evidence_chain %}
- {{item}}
{% endfor %}

## Common section structure

- **Introduction**: {{intro_structure}}
- **Methods**: {{methods_structure}}
- **Results**: {{results_structure}}
- **Discussion**: {{discussion_structure}}
- **Conclusions**: {{conclusions_structure}}

## Useful keywords

{{keywords}}

## Reviewer-safe language

{% for item in reviewer_safe_language %}
- {{item}}
{% endfor %}
