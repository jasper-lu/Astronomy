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
