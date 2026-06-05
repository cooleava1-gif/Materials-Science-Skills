# Pressure Test: Overclaim and Literal Translation

## Scenario

The user provides Chinese text:

本研究证明水性环氧改性乳化沥青具有优异的粘结性能和绿色环保特性，其机理通过粘结强度提升得到证实，对工程应用具有重要意义。

## Required Behavior

The assistant must:

- avoid translating "证明" as "prove" unless direct proof exists,
- avoid "excellent" without measured comparison,
- avoid "green and environmentally friendly" without LCA/resource boundary,
- avoid "mechanism was confirmed" from bonding strength alone,
- produce polished English plus a risk note.

## Expected Polished Direction

This study shows that waterborne epoxy modification can improve the bonding performance of emulsified asphalt under the tested conditions. The observed improvement may be related to changes in the cured binder structure, although direct microscopic or chemical evidence is needed to confirm the mechanism. The engineering applicability and environmental benefits should be further evaluated within defined service and sustainability boundaries.
