(* module A = Archimedes *)

let mass_sun = 1.989 *. (10. ** 30.);;
(* In terms of multiple of the mass of our sun *)
let our_min_mass = 0.8;;
let our_max_mass = 50.;; 

(* Returns IMF-form function for a given bound, alpha, and usage-specific adjustment
 * Adjustment is for changing into forms such as Luminosity instead of Number, etc *
 *
 * NOTE: We derive the constants using methods from these lecture notes:
 * https://websites.pmc.ucsc.edu/~glatz/astr_112/lectures/notes19.pdf
 * For our purposes, we take maximum mass to be 50 solar mass, and minimum to be 0.8 solar mass.
 *)

(* Now create IMF derivatives 
 * These have the exp at the front to mimic if it were found through integration *)
let power_diff low high exp = exp *. (high ** exp -. low ** exp);;

let fraction_lum low high = power_diff low high 2.15;;

let fraction_mass low high = power_diff low high (-.0.35);;

let fraction_num low high = power_diff low high (-.1.35);;

(* This function gets us the mass of the star to die most recently at time t (in 10Myrs) *)
let mass_death_at_time (t : float) : float = 
    if t = 0. then our_max_mass
    else 
        let div = t /. 1000. in 
        div ** (-.1. /. 2.5);;

(* t is in units of 10 Myrs.
 * Function will return as a fraction of a starting Luminosity *)
let stellar_luminosity (t : float) : float = 
    fraction_lum 0. (max 0.8 (mass_death_at_time t));;

(* We need to convert this into Magnitude.
 * This gives us the different in magnitude from the start *)
let lum_0 = stellar_luminosity 0.;;

let abs_mag_diff (lum : float) : float = 
    -.2.5 *. (log10 (lum /. lum_0));;

let stellar_mag_at_time (t : float) : float = 
    abs_mag_diff (stellar_luminosity t);;


(* This is the for part 2 *)
let g_r (m : float) = log (((m +. 2.) /. m) -. 0.65);;

let g_r_at_time (t: float) : float = 
    let high = mass_death_at_time t in 
    let avg = (fraction_mass our_min_mass high) /. (fraction_num our_min_mass high) in  
    g_r avg;;
