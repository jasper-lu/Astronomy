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

let plotA = initPlot "DECvsRA.png" "RA" "DEC" in 
A.Axes.box plotA;
A.Array.xy plotA data.(0) data.(1);
A.close plotA;;

let plotA = initPlot "MrvsZ.png" "Redshift" "Mr" in
A.Axes.box plotA;
A.Viewport.yrange plotA (-.25.) (-.17.);
A.Array.xy plotA data.(2) data.(4);
A.close plotA;;

let (gr, nBlues) = Util.get_gr_data data;;
let x = Util.make_range 2. 0.01;;

let plotB = initPlot "GRdistro.png" "g-r" "Number" in
A.Axes.box plotB;
A.Array.xy plotB ~style: (`Lines) ~fill: true ~fillcolor: (A.Color.blue) x gr;
(* A.Viewport.text plotB 0.1 20000. ("Fraction of blue galaxies is: " ^ (String.sub (string_of_float (nBlues)) 0 4)) ~pos: (A.Backend.RB);*)
A.Viewport.text plotB 0.1 20000. ("Fraction of blue galaxies is: " ^ (string_of_float nBlues)) ~pos: (A.Backend.RB);
A.Viewport.text plotB 0.1 17000. "Granularity is 0.01 gr" ~pos: (A.Backend.RB);
A.close plotB;;

let dn = Util.get_dndmr data 0. 0.1 0.;;
let mrX = Util.make_range 30. (-.0.1);;

let plotC = initPlot "MrDensity.png" "Mr" "log(dn/dMr)" in 
A.Axes.box plotC;
A.Array.xy plotC ~style: (`Lines) mrX dn;
A.close plotC;;

let to_string x mr = 
    let (a, b, c) = x in 
    "Data for mr " ^ (string_of_float mr) ^ " is " ^ (string_of_float a) ^ " " ^ (string_of_float b) ^ " " ^ (string_of_float c)
;;

let mr18Data = Util.get_volume_limited_data (-.18.) data;;
let mr19Data = Util.get_volume_limited_data (-.19.) data;;
let mr20Data = Util.get_volume_limited_data (-.20.) data;;
print_endline (to_string mr18Data (-.18.));; 
print_endline (to_string mr19Data (-.19.));;
print_endline (to_string mr20Data (-.20.));;

let (z18, _, _) = mr18Data;;
let (z19, _, _) = mr19Data;;
let (z20, _, _) = mr20Data;;

let dn18 = Util.get_dndmr data 0.025 z18 (-.18.);;
let dn19 = Util.get_dndmr data 0.025 z19 (-.19.);; 
let dn20 = Util.get_dndmr data 0.025 z20 (-.20.);; 

let plotE = initPlot "VolLimitedMrDensity.png" "Mr" "log(dn/dMr)" in
A.Axes.box plotE;
A.Array.xy plotE mrX dn18 ~fill: true ~style: (`Lines) ~fillcolor: (A.Color.yellow);
A.Array.xy plotE mrX dn19 ~fill: true ~style: (`Lines) ~fillcolor: (A.Color.red);
A.Array.xy plotE mrX dn20 ~fill: true ~style: (`Lines) ~fillcolor: (A.Color.blue);
A.close plotE;;

let plotE = initPlot "VolLimitedMrDensityNoCol.png" "Mr" "log(dn/dMr)" in
A.Axes.box plotE;
A.Array.xy plotE mrX dn18 ~style: (`Lines) ~fillcolor: (A.Color.yellow);
A.Array.xy plotE mrX dn19 ~style: (`Lines) ~fillcolor: (A.Color.red);
A.Array.xy plotE mrX dn20 ~style: (`Lines) ~fillcolor: (A.Color.blue);
A.close plotE;;

let dn = Util.get_dndmr_weighted data;;
let mrX = Util.make_range 30. (-.0.1);;

let plotF = initPlot "WeightedDensity.png" "Mr" "log(dn/dMr)" in 
A.Axes.box plotF;
A.Array.xy plotF ~style: (`Lines) mrX dn;
A.close plotF;;
