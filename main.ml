module A = Archimedes

let part1 = A.init ["Cairo";"PNG";"MagToTime.png"];;
A.Axes.box part1;
A.Viewport.yrange part1 0. 10.;
A.Viewport.xlabel part1 "Time (Gigayears)";
A.Viewport.ylabel part1 "M(t) - M(0)";
A.fx part1 Util.stellar_mag_at_time 0. 10.;
A.close part1;;

let part2 = A.init ["Cairo";"PNG";"G_RToTime.png"];;
A.Axes.box part2;
A.Viewport.xlabel part2 "Time (Gigayears)";
A.Viewport.ylabel part2 "g-r";
A.fx part2 Util.g_r_at_time 0. 10.;
A.close part2;;

let mag_to_gr (t : float) = (Util.g_r_at_time t, Util.stellar_mag_at_time t);;

let t_list = [0.01;0.1;1.;2.;5.;10.] in
let t_arr = Array.of_list t_list in
let t_label = ["10 Myr"; "100 Myr"; "1 Gyr"; "2 Gyr"; "5 Gyr"; "10 Gyr"] in 
let t_label_arr = Array.of_list t_label in
let gr = Array.make 6 0. in
let mag = Array.make 6 0. in

for i = 0 to 5 do 
    gr.(i) <- Util.g_r_at_time (t_arr.(i));
    mag.(i) <- Util.stellar_mag_at_time (t_arr.(i));
done;

let part3 = A.init ["Cairo";"PNG";"MagToG_R.png"] in 
A.Axes.box part3; 
A.Viewport.xlabel part3 "g-r";
A.Viewport.ylabel part3 "M(t) - M(0)";
A.xyf ~n:2000 part3 mag_to_gr 0. 10.;
A.Array.xy part3 gr mag;
let label = A.Backend.RB in
for i = 0 to 5 do 
    A.Viewport.text part3 (gr.(i)) (mag.(i)) (t_label_arr.(i)) ~pos: label;
done;
A.close part3;;
