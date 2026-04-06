let nth_bit num n = (num lsr n) land 1

let get_most_common_bit nums n equality_handler =
  let rec iter nums (zero_count, one_count) =
    match nums with
    | [] -> (zero_count, one_count)
    | head :: rest -> if nth_bit head n = 0 then iter rest (zero_count + 1, one_count) else iter rest (zero_count, one_count + 1)
  in 
  let (zero_count, one_count) = iter nums (0, 0) in
  if zero_count > one_count then
    0
  else if zero_count < one_count then
    1
  else
    equality_handler ()


let gamma nums bit_count =
  let equality_handler () = 
    assert false
  in
  let rec comp curr idx =
    if idx >= bit_count then curr else comp (curr + ((get_most_common_bit nums idx equality_handler) lsl idx)) (idx + 1)
  in comp 0 0

let epsilon nums bit_count = ((1 lsl bit_count) - 1) lxor (gamma nums bit_count)

let find_rating nums bit_count criteria =
  let rec helper curr_nums pos =
    match curr_nums with
    | [] -> assert false
    | [single] -> single
    | first :: rest ->
      if pos < 0 then
        assert false
      else
        let required = criteria curr_nums pos in
        helper (List.filter (fun el -> nth_bit el pos = required) curr_nums) (pos - 1)
  in helper nums (bit_count - 1)
    
let oxygen_generator_rating nums bit_count =
  let criteria nums bit_count = get_most_common_bit nums bit_count (fun () -> 1) in
  find_rating nums bit_count criteria

let co2_scrubber_rating nums bit_count =
  let criteria nums bit_count = (1 - get_most_common_bit nums bit_count (fun () -> 1)) in
  find_rating nums bit_count criteria

let part1 nums bit_count =
  (gamma nums bit_count) * (epsilon nums bit_count)

let part2 nums bit_count =
  (oxygen_generator_rating nums bit_count) * (co2_scrubber_rating nums bit_count)

let () = 
  let rec read_all_lines ic =
    match In_channel.input_line ic with
    | None -> ([], 0)
    | Some line -> let (list_part, _) = read_all_lines ic in ((int_of_string ("0b" ^ line) :: list_part), (String.length line)) 
  in
  let (nums, bit_count) = In_channel.with_open_text "input.txt" read_all_lines in
  Printf.printf "Part 1: %i\n" (part1 nums bit_count);
  Printf.printf "Part 2: %i\n" (part2 nums bit_count)