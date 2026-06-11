# Digest: BMRL "On the essential minimum of Faltings' height" (arXiv:1609.00071, Math. Comp. 87 (2018) 2425-2459)

Authors: Burgos Gil, Menares, Rivera-Letelier. PDF: literature/pdfs/bmrl_faltings_1609.00071.pdf.
Extracted text: /tmp/bmrl.txt (81k chars). Fetched & digested R2 (resolves the R1 Angle-4 gate).

## What it achieves
Computes the essential minimum mu_ess of the (stable) Faltings height on the moduli of
elliptic curves to 5-6 decimals (registry quotes -0.748629 <= mu_ess <= -0.748622), and
proves Faltings' height takes >=2 values below mu_ess (so it is NOT lower-semicontinuous,
unlike Weil/Neron-Tate). Numerical evidence: 4 isolated values before mu_ess.

## The LOWER-bound method = the SAME Smyth/Doche/Zagier auxiliary-function method
Section "Lower bounds through real sections" (Prop 6.x): the height of a point x is bounded by
  hF(x) >= inf_y g_s(y),   g_s(y) = -log ||s(y)||_Pet,
for any "real global section" s = (x) s_k^{a_k} (a_k > 0, weight 1), where x not in |div(s)|
(a FINITE set). This is EXACTLY Smyth's auxiliary-function / minimax method:
  - real section s = prod s_k^{a_k}   <->  Flammang's auxiliary product prod Q_j^{c_j};
  - weight-1 normalization                <->  the height normalization;
  - Green function g_s = -log||s||         <->  Flammang's f(z);
  - "x not in |div(s)|, a finite set"      <->  the integrality / finite-exception argument.
The authors state this explicitly: "this method was used in the aforementioned papers of Doche
and Zagier and can be traced back to ... results on Mahler measures by Smyth [Sm]."
=> BMRL contributes NO new lower-bound mechanism over Flammang/Smyth.

## The genuinely novel machinery (and why it does NOT transfer to Zhang-Zagier)
The "6-digit closing" rests on a tight approximation of the HYPERBOLIC GREEN FUNCTION g_hyp on
the modular curve of level one (which has no closed form), established via the Koebe distortion
theorem for univalent functions (Prop B). For Zhang-Zagier the Green function
g = log+|z| + log+|1-z| is ALREADY elementary and exact -- there is nothing to approximate, so
this machinery is inapplicable.

## The one structural idea (and why it does not fit ZZ either)
BMRL sharpen the bound by PENALIZING a single binding algebraic point (j=0) with a real weight
a = d/dx g_hyp(1), calibrated to the Green-function derivative there, so the min of the
penalized g_s is attained only at that point (their s = j^a * Delta, refined to
s = j^{a1}(j-1)^{a2} Delta). ZZ's binding locus is a DENSE equioscillation band (~25 points,
t in [0.49,2.83]; verified R2), not a single point, so this single-point sharpening does not
apply.

## Verdict for 82a (Angle-4 gate, resolved)
BMRL transfer is CLOSED. It is the same Smyth method; its novel ingredient is modular-curve
Green-function approximation, irrelevant when the ZZ Green function is explicit. Do not build it.
