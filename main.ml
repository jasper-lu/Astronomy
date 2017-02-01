module A = Archimedes

let part1 = A.init ["Cairo";"PNG";"MagToTime.png"];;
A.Axes.box part1;
A.fx part1 Util.stellar_mag_at_time 0. 1000.;
A.close part1;;

let part2 = A.init ["Cairo";"PNG";"G_RToTime.png"];;
A.Axes.box part2;
A.fx part2 Util.g_r_at_time 0. 1000.;
A.close part2;;

print_endline "REACHED AFTER ARRAY INIT ";; 
let mag = Array.make 100 0.;;
let g_r = Array.make 100 0.;;
print_endline "REACHED AFTER ARRAY INIT ";; 
for i = 0 to 99 do mag.(i) <- Util.stellar_mag_at_time (float_of_int(i * 10)); g_r.(i) <- Util.g_r_at_time (float_of_int(i * 10)) done;

print_endline "REACHED AFTER ARRAY INIT ";; 
let part3 = A.init ["Cairo";"PNG";"MagToG_R.png"] in 
A.Axes.box part3; 
A.Array.xy part3 g_r mag;
A.close part3;;
