module IntMap = Map.Make(Int)

let rec calc_pop_after_generations age gen_count memo =
  if age >= gen_count then (1, memo)
  else if age > 0 then
    calc_pop_after_generations 0 (gen_count - age) memo
  else match IntMap.find_opt gen_count memo with
  | Some memoized_val -> (memoized_val, memo)
  | None -> 
    let (parent_result, new_memo) = calc_pop_after_generations 6 (gen_count - 1) memo in
    let (child_result, new_memo) = calc_pop_after_generations 8 (gen_count - 1) new_memo in
    let new_memo = IntMap.add gen_count (parent_result + child_result) new_memo in
    (parent_result + child_result, new_memo)

let count_fish_after_time ages days =
  let memo = IntMap.empty in
  let (final_count, _) = List.fold_left (fun (count, curr_memo) age -> 
  let pop, new_memo = calc_pop_after_generations age days curr_memo in
  (count + pop, new_memo)
  ) (0, memo) ages in
  final_count

let part1 ages =
  count_fish_after_time ages 80

let part2 ages = 
  count_fish_after_time ages 256

let () = 
  let ages = In_channel.with_open_text "input.txt" 
  (fun ic -> 
    match In_channel.input_line ic with
    | None -> assert false
    | Some line -> List.map (int_of_string) (String.split_on_char ',' line)
  ) in
  Printf.printf "Part 1: %i\n" (part1 ages);
  Printf.printf "Part 1: %i\n" (part2 ages)