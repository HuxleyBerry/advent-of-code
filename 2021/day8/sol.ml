module IntMap = Map.Make(Int)
module IntSet = Set.Make(Int)

let count_unique_digits output_values =
  List.fold_left (fun acc value ->
    let to_add = match String.length value with
    | 2 | 4 | 3 | 7 -> 1
    | _ -> 0
    in acc + to_add
  ) 0 output_values

let part1 puzzles =
  List.fold_left (fun acc puzzle ->
    let _, outputs = puzzle in
    acc + count_unique_digits outputs
  ) 0 puzzles

(*let digit_data = [|[|'a';'b';'c';'e';'f';'g'|];
                  [|'c';'f'|];
                  [|'a';'c';'d';'e';'g'|];
                  [|'a';'c';'d';'f';'g'|];
                  [|'b';'c';'d';'f'|];
                  [|'a';'b';'d';'f';'g'|];
                  [|'a';'b';'d';'e';'f';'g'|];
                  [|'a';'c';'f'|];
                  [|'a';'b';'c';'d';'e';'f';'g'|];
                  [|'a';'b';'c';'d';'f';'g'|]|]*)

let digit_data = [|[|true;true;true;false;true;true;true|];
                  [|false;false;true;false;false;true;false|];
                  [|true;false;true;true;true;false;true|];
                  [|true;false;true;true;false;true;true|];
                  [|false;true;true;true;false;true;false|];
                  [|true;true;false;true;false;true;true|];
                  [|true;true;false;true;true;true;true|];
                  [|true;false;true;false;false;true;false|];
                  [|true;true;true;true;true;true;true|];
                  [|true;true;true;true;false;true;true|];|]

let digit_segment_counts = Array.map (Array.fold_left (fun acc segment_on -> acc + (if segment_on then 1 else 0)) 0) digit_data

let char_to_index c =
  int_of_char c - 97

let does_wiring_candidate_map_input_into_digit wiring_candidate digit input =
  let rec calc idx =
    if idx = String.length input then true
    else begin
      let c = input.[idx] in
      let _dest =  IntMap.find_opt (char_to_index c) wiring_candidate in
      let contained = match _dest with
      | None -> true
      | Some dest -> digit_data.(digit).(dest)
      in
      if not contained then false
      else calc (idx + 1)
    end
  in calc 0

let does_wiring_candidate_map_input_into_any_digit wiring_candidate input =
  let rec calc digit =
    if digit > 9 then false
    else if digit_segment_counts.(digit) != String.length input 
          || not (does_wiring_candidate_map_input_into_digit wiring_candidate digit input) then 
      calc (digit + 1)
    else true
  in calc 0

let find_digit wiring input =
  let rec calc digit =
    if digit > 9 then None
    else if digit_segment_counts.(digit) != String.length input then calc (digit + 1)
    else if does_wiring_candidate_map_input_into_digit wiring digit input then
      Some digit
    else 
      calc (digit + 1)
  in calc 0


let is_wiring_candidate_valid_so_far inputs wiring_candidate =
  List.for_all (does_wiring_candidate_map_input_into_any_digit wiring_candidate) inputs
                  
let decode_puzzle puzzle =
  let all_inputs, inputs_to_decode = puzzle in
  let rec calc wiring_candidate source_idx already_mapped_to =
    if is_wiring_candidate_valid_so_far all_inputs wiring_candidate then
      if source_idx > 6 then Some wiring_candidate
      else
        let rec calc2 dest_index =
          if dest_index > 6 then None
          else if IntSet.mem dest_index already_mapped_to then calc2 (dest_index + 1)
          else 
            let res = calc (IntMap.add source_idx dest_index wiring_candidate) (source_idx + 1) (IntSet.add dest_index already_mapped_to) in
            match res with
            | None -> calc2 (dest_index + 1)
            | Some solution -> Some solution
        in calc2 0
    else None
  in
  let discovered_wiring = calc IntMap.empty 0 IntSet.empty in
  match discovered_wiring with
  | None -> assert false
  | Some wiring -> List.fold_left (fun acc input -> 
      match find_digit wiring input with
      | None -> assert false
      | Some digit -> 10*acc + digit
    ) 0 inputs_to_decode


let part2 puzzles =
    List.fold_left (fun acc puzzle ->
    acc + decode_puzzle puzzle
  ) 0 puzzles

let () =
  let parse_line line =
    let bar_index = String.index line '|' in
    let wiring_combinations_string = String.sub line 0 (bar_index - 1) in
    let to_decode_string = String.sub line (bar_index + 2) (String.length line - bar_index - 2) in
    (String.split_on_char ' ' wiring_combinations_string, String.split_on_char ' ' to_decode_string)
  in

  let rec read_file ic =
    match In_channel.input_line ic with
    | None -> []
    | Some line -> parse_line line :: read_file ic
  in
    
  let puzzles = In_channel.with_open_text "input.txt" read_file in
  (*let (all_inputs, _) = List.nth puzzles 0 in
  let test_map = IntMap.of_seq @@ List.to_seq [(3,0);(4,1);(0,2);(5,3);(6,4);(1,5)] in
  print_endline @@ string_of_bool @@ is_wiring_candidate_valid_so_far all_inputs test_map;
  print_endline @@ string_of_bool @@ does_wiring_candidate_map_input_into_any_digit test_map "fbcad";
  print_endline @@ string_of_bool @@ does_wiring_candidate_map_input_into_digit test_map 3 "fbcad";*)
  Printf.printf "Part 1: %i\n" (part1 puzzles);
  Printf.printf "Part 2: %i\n" (part2 puzzles)