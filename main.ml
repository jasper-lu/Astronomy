module A = Archimedes

let part1 = A.init ["Cairo";"PNG";"MagToTime.png"];;
A.Axes.box part1;
A.fx part1 Util.stellar_mag_at_time 0. 1000.;
A.close part1;;

let part2 = A.init ["Cairo";"PNG";"G_RToTime.png"];;
A.Axes.box part2;
A.fx part2 Util.g_r_at_time 0. 1000.;
A.close part2;;

let mag_to_g_r (t : float) = (Util.g_r_at_time t, Util.stellar_mag_at_time t) in 

let part3 = A.init ["Cairo";"PNG";"MagToG_R.png"] in 
A.Axes.box part3; 
(*A.Array.xy ~style: `Lines part3 g_r mag;*)
A.xyf ~n:2000 part3 mag_to_g_r 0. 1000.;
A.close part3;;
