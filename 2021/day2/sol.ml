let part1 commands =
  let rec move commands pos =
    let (x, y) = pos in
    match commands with
    | [] -> pos
    | (direction, distance) :: rest -> 
      match direction with
      | "forward" -> move rest (x + distance, y)
      | "up" -> move rest (x, y - distance)
      | "down" -> move rest (x, y + distance)
      | _ -> assert false
  in
  let (final_x, final_y) = move commands (0, 0) in
  final_x * final_y

let part2 commands =
  let rec move commands state = 
    let (x, y, aim) = state in
    match commands with
    | [] -> state
    | (direction, distance) :: rest -> 
      match direction with
      | "forward" -> move rest (x + distance, y + aim * distance, aim)
      | "up" -> move rest (x, y, aim - distance)
      | "down" -> move rest (x, y, aim + distance)
      | _ -> assert false
  in
  let (final_x, final_y, _) = move commands (0, 0, 0) in
  final_x * final_y

let () =
  let parse_line line =
    match String.split_on_char ' ' line with
    | first :: second :: rest -> (first, int_of_string(second))
    | _ -> assert false
  in
  let rec read_all_lines ic =
    match In_channel.input_line ic with
    | None -> []
    | Some line -> (parse_line line) :: read_all_lines ic
  in
  let commands = In_channel.with_open_text "input.txt" read_all_lines in
  Printf.printf "Part 1: %i\n" (part1 commands);
  Printf.printf "Part 2: %i\n" (part2 commands)