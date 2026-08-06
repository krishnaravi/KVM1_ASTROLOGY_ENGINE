# Phase 7 Architecture: Rule Engine Framework

## Overview

Phase 7 implements the Rule Engine Framework, rule categories, `RuleRegistry`, and priority-based evaluation.

```
+------------------+   +-------------------+   +-------------------+
|CalculationContext|   |VedicEngine Output |   |   Varga Output    |
+--------+---------+   +---------+---------+   +---------+---------+
         |                       |                       |
         +-----------------------+-----------------------+
                                 |
                                 v
                     +-----------------------+
                     |      RuleEngine       |
                     +-----------+-----------+
                                 |
         +-----------------------+-----------------------+
         | (Priority Sort: Descending Execution Order)    |
         v                                               v
+------------------+                           +-------------------+
|  Priority 350    |                           |    Priority 80    |
|  Neecha Bhanga   |  ...  ...  ...  ...  ...  | FunctionalDignity |
+------------------+                           +-------------------+
```

## Rule Taxonomy Categories

1. **`classical`**: Base Parashari classical rules (e.g. Kendra placements).
2. **`yoga`**: General planetary combination rules (e.g. Budha-Aditya Yoga).
3. **`raja_yoga`**: Power and authority rules (e.g. Kendra-Kona lord conjunctions).
4. **`dhana_yoga`**: Wealth & prosperity rules (e.g. 2nd-11th lord associations).
5. **`arishta`**: Affliction and obstacle rules (e.g. Malefics in Dusthanas 6, 8, 12).
6. **`neecha_bhanga`**: Cancellation of debilitation rules.
7. **`functional_dignity`**: Functional benefic/malefic classifications per Lagna.
