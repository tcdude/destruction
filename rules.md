# Rules

## Initial, abstract idea

Inspired by Conways' Game of Life, my goal is to create a simulation game
for 1 or 2 players. The player can modify stats/rules of it's *species* and 
place a number of cells as starting formation. Afterwards the simulation 
runs until the first species goes extinct.

Each field in the grid has an equal amount of nutrition available. If a life
cell is on the field at the end of a simulation step, the cell consumes the 
amount it needs to survive, if enough nutrition remains, otherwise it dies.
On fields that are empty at the end of a simulation step, 1 unit of
nutrition is restored if not at full capacity.

During a simulation step, every field is evaluated against its direct
neighbours. If a life cell currently occupies the field, it is determined
whether the cell and its neighbouring siblings have more strength than the
neighbouring opposing species, thus surviving to the feeding, otherwise
the cell dies and gets replaced by a cell from the other species. 

## Stats / Rules

| Type | Value Range | Effect |
| ---- | ----------- | ------ |
| Strength | 1..3 | Adds to attack strength at the cost of more nutrition |
| Fertility | 1..3 | Number of adjacent cells needed for reproduction. Higher numbers reduce need for nutrition |
| Start Population | 4..36 | Determined by combination of Strength and Fertility -> (4 - Strength + Fertility) ^ 2 |

## Simulation Loop

1. Fight
2. Reproduce
3. Feed

## Structure

### World

Class to keep track of the state of the world.

### Species

Class to store the stats of a species.

## Game Flow

1. Main Menu
    1. 2 Player
    2. (optional) Train AI
2. 2 Player
    1. (Player 1) Set Strength + Fertility
    2. (Player 1) Place Start Population
    3. (Player 2) repeat same steps
    4. Start Simulation
3. Train AI
    1. Show Current Best Simulation
    2. Update Stats
 
