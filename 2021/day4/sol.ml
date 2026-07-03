let find_first_bingo order grid first_so_far =
  (* rows *)
  for i = 0 to 4 do
    
  end

let part1 order grids =
  let locations = Array.init 25 (fun idx -> 0) in
  List.iteri (fun idx num ->
    locations.(num) <- idx
  ) order

let print_order num_list = 
  List.iter (fun num -> print_string ((string_of_int num) ^ " ")) num_list;
  print_endline ""

let print_grids grids = 
  List.iter (fun grid -> 
    Array.iter (fun row ->
      Array.iter (fun num ->
          print_string ((string_of_int num) ^ " ")
      ) row;
      print_endline ""
    ) grid;
    print_endline ""
  ) grids

let () =
  let read_bingo_grid ic = 
    let grid = Array.init 5 (fun i -> Array.init 5 (fun j -> 0)) in
    for i = 0 to 4 do
      let line = In_channel.input_line ic in
      match line with
      | None -> assert false
      | Some x -> 
        for j = 0 to 4 do
          grid.(i).(j) <- int_of_string @@ String.trim @@ String.sub x (j*3) 2;
        done
    done;
    grid
  in
  let read_all_lines ic = 
    let order_string = In_channel.input_line ic in
    match order_string with
    | None -> assert false
    | Some os ->
      let order = List.map int_of_string (String.split_on_char ',' os) in
      let rec read_all_bingo_grids ic grids_list =
        match In_channel.input_line ic with
        | None -> grids_list
        | Some line -> let grid = read_bingo_grid ic in grid :: read_all_bingo_grids ic grids_list
      in
      (order, (read_all_bingo_grids ic []))
  in
  let (order, grids) = In_channel.with_open_text "input.txt" read_all_lines in
  print_order order;
  print_grids grids;
  Printf.printf "Part 1: %i\n" (part1 order grids)