#!/bin/bash

worlds=("eater-world_1.json" "eater-world_2.json" "eater-world_3.json" "eater-world_4.json" "eater-world_5.json")
players=("AStarManhattanPlayer" AStarEuclideanPlayer "UCSPlayer" "IterativeDeepeningPlayer")

> output.txt

for world in "${worlds[@]}"; do
  for player in "${players[@]}"; do
    echo "Running gridrunner for World: $world, Player: $player"
    
    output=$(/usr/bin/time -v gridrunner --world EaterWorld --entry solver:"$player" --horizon 200 "worlds/$world" 2>&1)
    
    echo "$output" >> output.txt
    
    echo "Finished running gridrunner for World: $world, Player: $player"
  done
done
