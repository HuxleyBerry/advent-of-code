
module IntSet = Set.Make(Int)

let get_neighbours (x,y) width length =
  let unfiltered = [(x+1,y);(x-1,y);(x,y+1);(x,y-1)] in
  List.filter (fun (x', y') -> 0 <= x' && x' < width && 0 <= y' && y' < length) unfiltered

let is_low_point (x,y) width length heights =
  List.for_all (fun (x',y') -> heights.(y).(x) < heights.(y').(x')) (get_neighbours (x,y) width length)

let part1 heights =
  let length = Array.length heights in
  let width = Array.length heights.(0) in
  let rec recurse_length y sum_so_far =
    let rec recurse_width x sum_so_far = 
      if x = width then sum_so_far
      else
        let found_low_point = is_low_point (x,y) width length heights in
        let new_sum = if found_low_point then sum_so_far + 1 + heights.(y).(x) else sum_so_far in
        recurse_width (x+1) new_sum
    in
    if y = length then
      sum_so_far
    else
      let sum_of_row = recurse_width 0 0 in
      recurse_length (y+1) (sum_so_far + sum_of_row)
  in
  recurse_length 0 0

let pos_to_int (x,y) width =
  y * width + x


let dfs (x,y) width length heights =
  let visited = IntSet.singleton @@ pos_to_int (x,y) width in
  let rec dfs_inner (x,y) width length heights visited =
    let rec recurse_over_neighbours remaining_neighbours visited = 
      match remaining_neighbours with
      | [] -> visited
      | (x', y') :: rest -> 
        if heights.(y').(x') = 9 || IntSet.mem (pos_to_int (x',y') width) visited then
          recurse_over_neighbours rest visited
        else 
          let dfs_result_on_neighbour = dfs_inner (x',y') width length heights (IntSet.add (pos_to_int (x',y') width) visited) in
          recurse_over_neighbours rest dfs_result_on_neighbour
    in recurse_over_neighbours (get_neighbours (x,y) width length) visited
  in 
  let basin = dfs_inner (x,y) width length heights visited in
  IntSet.cardinal basin

let part2 heights = 
  let length = Array.length heights in
  let width = Array.length heights.(0) in
  let rec recurse_length y locations =
    let rec recurse_width x locations = 
      if x = width then locations
      else
        if is_low_point (x,y) width length heights then (
          recurse_width (x+1) ((x,y) :: locations)
        )
        else
          recurse_width (x+1) locations
    in
    if y = length then
      locations
    else
      recurse_length (y+1) (recurse_width 0 locations)
  in
  let low_points = recurse_length 0 [] in
  let basin_sizes = List.sort ( Fun.flip compare ) (List.map (fun (x,y) -> dfs (x,y) width length heights) low_points) in
  List.fold_left (fun acc value -> acc * value) 1 (List.filteri (fun i v -> i < 3) basin_sizes)


let () =
  let parse_line line =
    let rec parse_remaining idx =
      if idx < String.length line then (
        (int_of_char line.[idx] - int_of_char '0') :: (parse_remaining (idx + 1))
      )
      else
        []
    in 
    let as_list = parse_remaining 0 in
    Array.of_list as_list
  in

  let rec read_to_list ic =
    match In_channel.input_line ic with
    | None -> []
    | Some line -> (parse_line line) :: read_to_list ic
  in

  let read ic = Array.of_list @@ read_to_list ic in

  let heights = In_channel.with_open_text "input.txt" read in
  Printf.printf "Part 1: %i\n" (part1 heights);
  Printf.printf "Part 2: %i\n" (part2 heights)