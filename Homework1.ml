(*
module A = Archimedes

let vp = A.init ["Cairo";"PNG";"out.png"];;
A.Axes.box vp;
A.fx vp sin 0. 10.;
A.close vp
*)

let mass_sun = 1.989 *. (10. ** 30.);;

(* Returns IMF-form function for a given bound, alpha, and usage-specific adjustment
 * Adjustment is for changing into forms such as Luminosity instead of Number, etc *
 *
 * NOTE: We derive the constants using methods from these lecture notes:
 * https://websites.pmc.ucsc.edu/~glatz/astr_112/lectures/notes19.pdf
 * For our purposes, we take maximum mass to be 50 solar mass, and minimum to be 0.8 solar mass.
 *)


let initial_mass_integrated (min : float) (max : float) (alpha : float) (adj : float) : float -> float -> float =  
    let exp = -.alpha +. adj +. 1. in 
    let pow x = x ** exp in 
    let limit_diff = pow min -. pow max in 
    let constant = -.exp /. limit_diff in 
    let f m1 m2 = 
        let diff = pow m2 -. pow m1 in 
        let coeff = constant /. exp in 
        coeff *. diff 
    in 
    f
;;
    
(* set the imf to our bounds *)
let bounded_imf = initial_mass_integrated 0.1 120.;;

(* we are using salpeter *)
let imf_salpeter = bounded_imf 2.35;;

(* Now create IMF derivatives *)
let fraction_count = imf_salpeter 0.0;;

let fraction_lum = imf_salpeter 3.5;;

let fraction_mass = imf_salpeter 1.;;



(* t is in units of 10 Myrs.
 * Function will return as a fraction of a starting Luminosity *)
(*
let stellar_luminosity (t: int) : float = 
    3.0
    *)


(* test *)
let print_float_nl f = print_float f; print_newline ();;
print_endline "Testing for a variety of ranges. Should see a quick drop in number";
print_float_nl (fraction_count 0.1 120.); 
print_float_nl (fraction_count 0.5 120.); 
print_float_nl (fraction_count 1. 120.); 
print_float_nl (fraction_count 3. 120.); 
print_float_nl (fraction_count 6. 120.); 

