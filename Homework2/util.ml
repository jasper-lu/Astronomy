let pi = 4.0 *. atan 1.0;;
(* Multiplier to convert from full sphere volume to sdss volume *)
let c = 2.295 /. (4. *. pi);;

(* HELPER METHODS FOR FILE *)
let make_range max steps = 
    let len = abs (int_of_float (max /. steps)) in 
    let data = Array.make len 0. in 
    for x = 1 to (len - 1) do 
        data.(x) <- (data.(x - 1) +. steps)
    done;
    data 
;;

(* Returns volume in terms of Mpc^3 * h^-3 *)
let get_vol_between_shifts lower upper = 
    let inferred_dist z = 
        let c = 299792. in 
        z *. c /. 100. 
    in
    let vol r = (4. /. 3.) *. pi *. (r ** 3.) in 
    (vol (inferred_dist upper)) -. (vol (inferred_dist lower))
;;

(* QUESTION C *)

let get_gr arr =
    let data = Array.make (Array.length (arr.(0))) 0. in 
    for x = 0 to (Array.length data - 1) do 
        (*data.(x) <- (float_of_int (int_of_float (arr.(3).(x) *. 100.) - (int_of_float (arr.(4).(x) *. 100.))));*)
        data.(x) <- (arr.(3).(x) *. 100.) -. (arr.(4).(x) *. 100.);
    done;
    data
;;

let get_gr_bucket x bucket_size = 
    (*truncate (x /. bucket_size) *)
    int_of_float x
;;

let get_gr_n arr = 
    let gran = 0.01 in 
    let size = int_of_float (2. /. gran) in 
    let data = Array.make size 0. in 
    for x = 0 to (Array.length arr - 1) do 
        let index = get_gr_bucket (arr.(x)) gran in 
        if index < size && index >= 0  then 
            data.(index) <- (data.(index) +. 1.)
    done;
    data
;;

let frac_blue gr_arr threshold = 
    let n = Array.fold_left (fun acc x -> if x < threshold then acc +. 1. else acc) 0. gr_arr in 
    n /. (float_of_int (Array.length gr_arr))
;;

let get_gr_data arr = 
    let gr_arr = get_gr arr in 
    (get_gr_n gr_arr, frac_blue gr_arr 75.)


let make_gr_range = 
    let data = Array.make 1200 0. in 
    data.(0) <- (-.5.);
    for x = 1 to 999 do
        data.(x) <- (data.(x - 1) +. 0.01) 
    done; 
    data 
;;

let get_mr_bucket x = 
    let x = -.x in 
    int_of_float (x *. 10.)
;;

(*LUMINOSITY FUNCTION GRAPHS *)
let get_n_by_mr arr z_low z_lim mr = 
    let data = Array.make 300 0. in
    for x = 0 to (Array.length (arr.(0)) - 1) do 
        if (arr.(2).(x)) < (z_lim) && (arr.(2).(x) > z_low) && (arr.(4).(x)) < mr then 
            let index = get_mr_bucket (arr.(4).(x)) in 
            data.(index) <- (data.(index) +. 1.)
    done;
    data
;;

let get_dndmr arr z_low z_lim mr = 
    let n_by_mr = get_n_by_mr arr z_low z_lim mr in 
    let vol = get_vol_between_shifts z_low z_lim in 
    let vol = vol *. c in 
    Array.iteri (fun i x -> n_by_mr.(i) <- (log10 (x /. vol))) n_by_mr;
    n_by_mr
;;

(* Question D *) 
let shift_lower_bound = 0.025;;

let get_shift_bound_for_mag (mr : float) arr = 
    let len = Array.length arr.(0) in 
    let curr_shift = ref 0. in 
    for x = 0 to (len - 1) do 
        if arr.(4).(x) > mr then 
            curr_shift := max (arr.(2).(x)) (!curr_shift)
    done;
    !curr_shift
;;

(* Could be immensely sped up if I combine all 3 passes into one *)
let get_volume_limited_data mr arr = 
    let upper = get_shift_bound_for_mag mr arr in 
    let len = Array.length arr.(0) in 
    let count = ref 0. in 
    let blue_count = ref 0. in 
    for x = 0 to (len - 1) do 
        if (arr.(2).(x)) > shift_lower_bound && (arr.(2).(x)) < upper then 
            begin
                count := (!count +. 1.);
                if (arr.(3).(x) -. arr.(4).(x)) < 0.75 then  
                    blue_count := (!blue_count +. 1.)
            end
    done;
    (upper, (!blue_count /. !count), get_vol_between_shifts shift_lower_bound upper *. c)

(* Question F *)
let get_dndmr_weighted arr = 
    let n_by_mr = get_n_by_mr arr 0. 0.1 0. in 
    let vol_for_mr mr = get_vol_between_shifts 0. (get_shift_bound_for_mag mr arr) *. c in 
    Array.iteri (fun i x -> n_by_mr.(i) <- (log10 (x /. (vol_for_mr (float_of_int i *. (-.0.1)))))) n_by_mr;
    n_by_mr
