# Flexi-clique
This is the implementation of flexi-clique, which is described in the following papaer:
- Flexi-clique: Exploring Flexible and Sub-linear Clique Structures

## How to use?
### A simple description for finding flexi-clique and some experiments are as follows:

### Peeling algorithm for the flexi-clique
[command for the tree type is in ()]
- Input parameters
  - Path of the hypergraph data
  - $\tau$
-Then the size of the flexi-clique and nodes containted in are saved.  
Example code for the index construction is below
```
python flexi_clique.py --file_path amazon.txt --tau 0.5
# the result will be saved within few seconds(minutes)
```

