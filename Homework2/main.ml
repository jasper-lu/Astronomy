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
        (*List.iteri (fun i d -> print_string d; print_char ' ') data_line;
        print_newline ();*)
        List.iteri (fun i d -> data.(i).(x) <- (float_of_string d); ()) data_line;
    done;
in

let plotA = initPlot "DECvsRA.png" "DEC" "RA" in 
A.Axes.box plotA;
A.Array.xy plotA data.(0) data.(1);
A.close plotA;;

let plotB = initPlot "MrvsZ.png" "Mr" "Redshift" in
A.Axes.box plotB;
A.Array.xy plotB data.(2) data.(4);
A.close plotB;;
