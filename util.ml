(* In terms of multiple of the mass of our sun *)
let our_min_mass = 0.08;;
let our_max_mass = 50.;; 

(* UTILS *)

let integrate f a b steps =
    let meth f x h = f (x +. h /. 2.) in 
    let h = (b -. a) /. float_of_int steps in
    let rec helper i s =
        if i >= steps then s
        else helper (succ i) (s +. meth f (a +. h *. float_of_int i) h)
    in
    h *. helper 0 0.
;;

(* Now create IMF derivatives 
 * These have the exp at the front to mimic if it were found through integration *)
let power_diff low high exp = (1. /. exp) *. (high ** exp -. low ** exp);;

let fraction_lum low high = power_diff low high 2.15;;

let fraction_mass low high = power_diff low high (-.0.35);;

let fraction_num low high = power_diff low high (-.1.35);;

(* This function gets us the mass of the star to die most recently at time t (in 10Myrs) *)
let mass_death_at_time (t : float) : float = 
    if t = 0. then our_max_mass
    else 
        let div = t /. 10. in 
        div ** (-.1. /. 2.5);;

(* t is in units of 10 Myrs.
 * Function will return as a fraction of a starting Luminosity *)
let stellar_luminosity (t : float) : float = 
    fraction_lum 0.08 (max 0.08 (mass_death_at_time t));;

(* We need to convert this into Magnitude.
 * This gives us the different in magnitude from the start *)
let lum_0 = stellar_luminosity 0.;;

let abs_mag_diff (lum : float) : float = 
    -.2.5 *. (log10 (lum /. lum_0));;

let stellar_mag_at_time (t : float) : float = 
    abs_mag_diff (stellar_luminosity t);;

(* This is for part 2 *)
let gr (m : float) : float = log ((m +. 2.) /. m) -. 0.65;;

let lum_ratio (m : float) : float = 
    let gr_val = gr m in 
    let lg = 10. ** (-.0.4 *. gr_val) in 
    let lr = m ** 3.5 in 
    lr *. lg
;;

(* This basically gets us our L_g *)
let lum_integrated min max = integrate lum_ratio min max 1000;;

(* This returns the g-r of a galaxy with mass between min and max *)
let gr_galaxy (min : float) (max : float) = 
    let weight = 3.5 in 
    (* This basically gets us our L_r *)
    let diff = integrate (fun x -> x ** 3.5) min max 1000 in
    (*let diff = max -. min in *)
    let lum_ratio_avg = (lum_integrated min max) /. diff in 
    -.2.5 *. (log10 lum_ratio_avg)    
;;

(* This returns the g-r for a galaxy at time t after formation *)
let g_r_at_time (t: float) : float = 
    gr_galaxy our_min_mass (mass_death_at_time t)
;;
