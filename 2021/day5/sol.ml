let custom_min num possible_num =
  match possible_num with
  | None -> num
  | Some num2 -> if num < num2 then num else num2

let custom_max num possible_num =
  match possible_num with
  | None -> num
  | Some num2 -> if num > num2 then num else num2

let get_grid_width_and_height locations =
  let rec util remaining_locations ((xMin, xMax), (yMin, yMax)) =
    match remaining_locations with
    | [] -> ((xMin, xMax), (yMin, yMax))
    | (x, y) :: rest -> util rest ((Some (custom_min x xMin), Some (custom_max x xMax)), (Some (custom_min y yMin), Some (custom_max y yMax)))
  in
  util locations ((None, None), (None, None))

let get_grid_width_and_height vents =
  let extremes = get_grid_width_and_height ((List.map (fun (left, right) -> left) vents) @ (List.map (fun (left, right) -> right) vents)) in
  match extremes with
  | (Some xMin, Some xMax), (Some yMin, Some yMax) -> (xMin, xMax), (yMin, yMax)
  | _ -> assert false

let print_grid grid =
  Array.iter (fun row -> Array.iter (fun num -> 
    if num = 0 then
      print_char '.'
    else
      print_string @@ string_of_int num
    ) row; print_char '\n') grid

let apply_lines vents consider_diagonal =
  let ((xMin, xMax), (yMin, yMax)) = get_grid_width_and_height vents in
  (* Printf.printf "%i %i %i %i\n" xMin xMax yMin yMax; *)
  let grid = Array.init (yMax - yMin + 1) (fun i -> Array.make (xMax - xMin + 1) 0) in
  let count = ref 0 in
  let update_grid grid x y =
    if grid.(y).(x) == 1 then
      count := !count + 1;
    grid.(y).(x) <- (grid.(y).(x) + 1)
  in
  List.iter (fun ((start_x, start_y), (end_x, end_y)) -> 
    if start_x = end_x then
      for y = min start_y end_y to max start_y end_y do
        let x_index = start_x - xMin in
        let y_index = y - yMin in
        update_grid grid x_index y_index
      done
    else if start_y = end_y then
      for x = min start_x end_x to max start_x end_x do
        let x_index = x - xMin in
        let y_index = start_y - yMin in
        update_grid grid x_index y_index
      done
    else if consider_diagonal && Int.abs (start_x - end_x) = Int.abs (start_y - end_y) then
      let size = Int.abs (start_x - end_x) in
      let x_direction = (end_x - start_x) / size in
      let y_direction = (end_y - start_y) / size in
      for i = 0 to size do
        let x_index = start_x - xMin + x_direction*i in
        let y_index = start_y - yMin + y_direction*i in
        update_grid grid x_index y_index
      done
    ) vents;
  (* print_grid grid; *)
  !count

let part1 vents =
  apply_lines vents false

let part2 vents =
  apply_lines vents true

let () =
  let split_num_pair pair_string =
    let comma_index = String.index pair_string ',' in
    (int_of_string @@ String.sub pair_string 0 comma_index, int_of_string @@ String.sub pair_string (comma_index + 1) (String.length pair_string - (comma_index+1)))
  in
  let read_line line = 
    let arrow_index = String.index line '>' in
    let left = String.sub line 0 (arrow_index - 2) in
    let right = String.sub line (arrow_index + 2) ((String.length line) - (arrow_index + 2)) in
    (split_num_pair left, split_num_pair right)
  in
  let rec read_all_lines ic = 
    match In_channel.input_line ic with
    | None -> []
    | Some line -> read_line line :: read_all_lines ic
  in
  let vents = In_channel.with_open_text "input.txt" read_all_lines in
  Printf.printf "Part 1: %i\n" (part1 vents);
  Printf.printf "Part 2: %i\n" (part2 vents)