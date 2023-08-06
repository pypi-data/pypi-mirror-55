# AxisProj
Axis-Aligned Decomposition of Linear Projections

## Installation 
```pip install axisproj```

#### From source:
`pip install -e .` or `python setup.py`


## Usage
```
from axisproj import LPPObjective, optiomal

objective = LPPObjective(knn=12,sigma=0.3)
lp, ap = optimal(X, objective)
```

Three linear projection objectives are defined in `axisproj.objective`
* LDEObjective
* LPPObjective
* PCAObjective

`optimal()` also accepts an optional histogram function. The default value
is generated using the `precision_recall.histogram` functor.

## Acknowledgment
This package is a rewrite of the LLNL code described in 

"Exploring High-Dimensional Structure via Axis-Aligned Decomposition of Linear Projections
Linear Axis-Aligned", J. J. Thiagarajan, S. Liu, K. N. Ramamurthy and P.-T. Bremer, EuroVis 2018