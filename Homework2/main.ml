open Printf 
open Str

module A = Archimedes 

let file = "SDSS_DR7.dat"

let initPlot s xl yl = 
    let plot = A.init["Cairo";"PNG";s] in 
    A.Viewport.xlabel plot xl; 
    A.Viewport.ylabel plot yl; 
    plot 
;;

let len = 550166;;
let data = Array.make_matrix 5 len 0.;;

let () = 
    let ic = open_in file in 
    for x = 0 to 550165 do 
        let line = input_line ic in 
        let data_line = Str.split (Str.regexp "[ \t]+") line in 
        List.iteri (fun i d -> data.(i).(x) <- (float_of_string d); ()) data_line;
    done;
in

let plotA = initPlot "DECvsRA.png" "DEC" "RA" in 
A.Axes.box plotA;
A.Array.xy plotA data.(0) data.(1);
A.close plotA;;

let plotB = initPlot "MrvsZ.png" "Redshift" "Mr" in
A.Axes.box plotB;
A.Viewport.yrange plotB (-.25.) (-.17.);
A.Array.xy plotB data.(2) data.(4);
A.close plotB;;

let (gr, nBlues) = Util.get_gr_data data;;
let x = Util.make_range 2. 0.01;;

let plotC = initPlot "GRdistro.png" "g-r" "Number" in
A.Axes.box plotC;
A.Array.xy plotC ~style: (`Lines) x gr;
A.Viewport.text plotC 0.1 20000. ("Fraction of blue galaxies is: " ^ (String.sub (string_of_float (nBlues)) 0 4)) ~pos: (A.Backend.RB);
A.Viewport.text plotC 0.1 17000. "Granularity is 0.01 gr" ~pos: (A.Backend.RB);
A.close plotC;;

let dn = Util.get_dndmr data;;
let mrX = Util.make_range 30. (-.0.1);;

let plotD = initPlot "MrDensity.png" "Mr" "log(dn/dMr)" in 
A.Axes.box plotD;
A.Array.xy plotD ~style: (`Bars 0.1) mrX dn;
A.close plotD;;

let to_string x = 
    let (a, b, c) = x in 
    (string_of_float a) ^ " " ^ (string_of_float b) ^ " " ^ (string_of_float c)
;;
print_endline (to_string (Util.get_volume_limited_data (-.18.) data));;
print_endline (to_string (Util.get_volume_limited_data (-.19.) data));;
print_endline (to_string (Util.get_volume_limited_data (-.20.) data));;
(*
let gr = Util.get_gr data in 
let min = Array.fold_left (fun a b -> if a < b then a else b) 30. gr in

let max = Array.fold_left (fun a b -> if a > b then a else b) (-.30.) gr in
print_float min;print_char ' ';print_float max;;
*)
