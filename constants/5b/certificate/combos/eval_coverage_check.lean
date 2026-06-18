import Constants.C5bBridgePerm
open C5b C5bBridgePerm
-- diffs4B constant across a few orderings of a sample 4-subset:
#eval diffs4B 0 136 200 243          -- one order
#eval diffs4B 243 200 136 0          -- reversed
#eval diffs4B 200 0 243 136          -- shuffled
#eval diffs4B 0 5 10 20              -- a non-(4,5) quadruple, one order
#eval diffs4B 20 10 0 5              -- same quadruple shuffled
