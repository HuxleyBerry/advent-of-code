let char_to_points_for_error c =
  match c with
  | ')' -> 3
  | ']' -> 57
  | '}' -> 1197
  | '>' -> 25137
  | _ -> assert false

let char_to_points_for_completion c =
  match c with
  | '(' -> 1
  | '[' -> 2
  | '{' -> 3
  | '<' -> 4
  | _ -> assert false

let get_expected_closer c =
  match c with
  | '(' -> ')'
  | '[' -> ']'
  | '{' -> '}'
  | '<' -> '>'
  | _ -> assert false

let is_opener c =
  match c with
  | '(' | '[' | '{' | '<' -> true
  | ')' | ']' | '}' | '>' -> false
  | _ -> assert false

let get_error_score line =
  let rec calc stack idx =
    if idx = String.length line then
      None
    else
      if is_opener line.[idx] then
          calc (line.[idx] :: stack) (idx+1)
      else
        match stack with
        | [] -> calc (line.[idx] :: stack) (idx+1)
        | top :: rest ->
          if get_expected_closer top != line.[idx] then
            Some (char_to_points_for_error line.[idx])
          else
            calc rest (idx+1)
  in calc [] 0

let get_completion_score line =
  let rec calc stack idx =
    if idx = String.length line then
      stack
    else
      if is_opener line.[idx] then
          calc (line.[idx] :: stack) (idx+1)
      else
        match stack with
        | [] -> calc (line.[idx] :: stack) (idx+1)
        | top :: rest ->
          if get_expected_closer top != line.[idx] then
            [] (* we can treat this as the stack being empty*)
          else
            calc rest (idx+1)
  in 
  let stack_at_completion = calc [] 0 in
  let rec get_score_from_reversed_stack reversed_stack =
    match reversed_stack with
    | [] -> 0
    | top :: rest -> 
      (5 * (get_score_from_reversed_stack rest)) + char_to_points_for_completion top
  in get_score_from_reversed_stack (List.rev stack_at_completion)

let part1 lines =
  List.fold_left (fun acc line -> 
    match get_error_score line with
    | None -> acc
    | Some score -> acc + score
  ) 0 lines

let part2 lines =
  let scores = List.sort compare (List.filter (fun x -> x != 0) (List.map get_completion_score lines)) in
  List.nth scores (((List.length scores) - 1)/2)

let () =
  let read ic =
    let rec read_remaining_lines lines_so_far =
      match In_channel.input_line ic with
      | None -> lines_so_far
      | Some line -> line :: read_remaining_lines lines_so_far
    in read_remaining_lines []
  in
  let lines = In_channel.with_open_text "input.txt" read in
  Printf.printf "Part 1: %i\n" (part1 lines);
    Printf.printf "Part 2: %i\n" (part2 lines)