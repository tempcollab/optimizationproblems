/-
Sketch slug: ghr-lemma-lean  (constant 3a, LOWER bound -- Lean-certifiable line).

The proof lives in `Sketches/Ghr.lean` (module name `Sketches.Ghr`, hyphen-free so Lean's
module-name grammar accepts it).  This file is the slug-named entry point required by the
repo convention; it re-exports the proof so `import Sketches.«ghr-lemma-lean»` also works.

Build target:        lake build Sketches.Ghr
Axiom check:         #print axioms C3a.beats_record
  => [propext, Classical.choice, Quot.sound]   (NO sorryAx, NO smuggled axiom)
-/
import Sketches.Ghr
