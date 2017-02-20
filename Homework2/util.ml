let get_gr arr =
    let data = Array.make (Array.length (arr.(0))) 0. in 
    for x = 0 to (Array.length data - 1) do 
        data.(x) <- (arr.(3).(x) -. arr.(4).(x));
    done;
    data
;;

let get_gr_bucket x = 
    int_of_float (x *. 100.)

let get_gr_n arr = 
    let data = Array.make 200 0. in 
    for x = 0 to (Array.length arr - 1) do 
        let index = get_gr_bucket (arr.(x)) in 
        if index < 200 && index >= 0  then 
            data.(index) <- (data.(index) +. 1.)
    done;
    data 
;;

let frac_blue gr_arr threshold = 
    let n = Array.fold_left (fun acc x -> if x >= 0.75 then acc +. 1. else acc) 0. gr_arr in 
    n /. (float_of_int (Array.length gr_arr))
;;

let get_gr_data arr = 
    let gr_arr = get_gr arr in 
    (get_gr_n gr_arr, frac_blue gr_arr 0.75)

let make_range max steps = 
    let len = abs (int_of_float (max /. steps)) in 
    let data = Array.make len 0. in 
    for x = 1 to (len - 1) do 
        data.(x) <- (data.(x - 1) +. steps)
    done;
    data 
;;

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

(* THIS QUESTION IS STILL WRONG, I'M SURE. WRONG UNITS *)
(* Multiplier to convert from 2.295 steradian coverage to 4.0 *)
let c = 4. /. 2.295;;

let get_dndmr arr = 
    let data = Array.make 300 0. in
    for x = 0 to (Array.length (arr.(0)) - 1) do 
        if (arr.(2).(x)) < (0.1) then 
            let index = get_mr_bucket (arr.(4).(x)) in 
            data.(index) <- (data.(index) +. 1.)
    done;
    Array.iteri (fun i x -> data.(i) <- (log10 (x *. c))) data;
    data
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

(* Returns volume in terms of Mpc^3 * h^-3 *)
let get_vol_between_shifts lower upper = 
    let inferred_dist z = 
        let c = 299792. in 
        z *. c /. 100. 
    in
    let pi = 4.0 *. atan 1.0 in 
    let vol r = (4. /. 3.) *. pi *. (r ** 3.) in 
    (vol (inferred_dist upper)) -. (vol (inferred_dist lower))
;;

(* Could be immensely sped up if I combine all 3 passes into one *)
let get_volume_limited_data mr_lower arr = 
    let upper = get_shift_bound_for_mag mr_lower arr in 
    let len = Array.length arr.(0) in 
    let count = ref 0. in 
    let blue_count = ref 0. in 
    for x = 0 to (len - 1) do 
        if (arr.(2).(x)) > shift_lower_bound && (arr.(2).(x)) < upper then 
            begin
                count := (!count +. 1.);
                if (arr.(3).(x) -. arr.(4).(x)) > 0.75 then  
                    blue_count := (!blue_count +. 1.)
            end
    done;
    print_endline (string_of_float !blue_count);
    print_endline (string_of_float !count);
    (upper, (!blue_count /. !count), get_vol_between_shifts shift_lower_bound upper)
