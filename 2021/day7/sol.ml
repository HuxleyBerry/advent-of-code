let rec calc curr_min curr_movement_required pos left_block_size right_block_size right_block =
  (* left_block <= pos and right_block > pos *)
  match right_block with
  | [] -> curr_min
  | front :: rest ->
    let movement_required = curr_movement_required + (front - pos)*left_block_size - (front - pos)*right_block_size in
    let min_so_far = min movement_required curr_min in
    min min_so_far (calc min_so_far movement_required front (left_block_size + 1) (right_block_size - 1) rest)

let part1 positions =
  let sum = List.fold_left (fun acc num -> acc + num) 0 positions in
  let size = List.length positions in
  match positions with
  | [] -> assert false
  | smallest :: rest ->
    let cost_to_move_everything_to_smallest = (sum - size*smallest) in
    calc cost_to_move_everything_to_smallest cost_to_move_everything_to_smallest smallest 1 (size - 1) rest

let get_cost_of_position_part2 submarine_pos positions =
  List.fold_left (fun acc crab_pos -> 
    let dist = Int.abs (submarine_pos - crab_pos) in
    acc + (dist)*(dist+1)/2
  ) 0 positions

let part2 positions =
  match positions with
  | [] -> assert false
  | smallest :: rest ->
    let min_pos = smallest in
    let max_pos = List.fold_left (fun acc num -> num) 0 positions in
    let large_enough_num = 100000000 in
    let seq = Seq.take (max_pos - min_pos - 1) (Seq.ints min_pos) in
    Seq.fold_left (fun acc potential_sub_pos -> Int.min acc (get_cost_of_position_part2 potential_sub_pos positions)) large_enough_num seq

let () = 
  let positions = In_channel.with_open_text "input.txt" (fun ic ->
    List.map int_of_string (String.split_on_char ',' (String.trim @@ In_channel.input_all ic))
  )
  in
  let positions = List.sort compare positions in (* increasing order *)
  Printf.printf "Part 1: %i\n" (part1 positions);
  Printf.printf "Part 2: %i\n" (part2 positions)