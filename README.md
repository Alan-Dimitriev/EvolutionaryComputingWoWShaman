# Using Evolutionary Computing To Find The Ideal Shaman Healing Spell Rotation In World of Warcraft

This study proposes the creation of an evolutionary algorithm to
find what the best single target healing spell rotation for shamans
in World of Warcraft is based on percent healing generated over a
given span of time. The algorithm implements a steady state model,
with tournament selection to find parents, applying one or two
point crossover and point mutations to the offspring. While the
globally optimal spell rotation was not uncovered, the proposed
algorithm seems capable of solving the task given more compute
power and time.

[The final paper can be viewed here](CISC_851_FINAL_PROJECT.pdf)

Executing the code:
To run the main evolutionary algorithm the python file can be ran as is. 
All implementation is included in the main() function.
Number of unique trials (n), number of iterations (vmax), size of population (pop_size) and length of rotations (individual length) can all be customized
Please note that the program does take more time for populations mapping a longer period of time.
To run the greedy algorithm used for comparison uncomment the specified lines.
Rest of the implementation should be rather straightwforward as the code is well documented.


Note: The output of my algorithm is a set of rather long rotations and their associated times making it really difficult to include them directly
into the paper itself. I have included my results in outputs.txt and based my conclusions and analysis of my model off of those trials.


