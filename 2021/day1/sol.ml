let rec part1 list =
  match list with
  | [] -> 0
  | [single] -> 0
  | first :: second :: rest -> if first < second then 1 + part1 (second :: rest) else part1 (second :: rest)

let rec part2 list =
  if List.length list <= 3 then
    0
  else
    match list with
    | a :: (b :: c :: d :: e as rest) -> if a < d then 1 + part2 rest else part2 rest
    | _ -> assert false

let () =
  let rec read_all_lines ic =
    match In_channel.input_line ic with
    | None -> []
    | Some line -> int_of_string(line) :: read_all_lines ic
  in
  let all_lines = In_channel.with_open_text "input.txt" read_all_lines in
  Printf.printf "Part 1: %i\n" (part1 all_lines);
  Printf.printf "Part 2: %i\n" (part2 all_lines)