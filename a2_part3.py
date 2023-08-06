"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Part 3)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 3 of this assignment. You should NOT make any changes to a2_minichess.py.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 Mario Badr, David Liu, and Isaac Waller.
"""
import random
from typing import Optional

import a2_game_tree
import a2_minichess


class ExploringPlayer(a2_minichess.Player):
    """A Minichess player that plays greedily some of the time, and randomly some of the time.

    See assignment handout for details.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]
    _exploration_probability: float

    def __init__(self, game_tree: a2_game_tree.GameTree, exploration_probability: float) -> None:
        """Initialize this player."""
        self._game_tree = game_tree
        self._exploration_probability = exploration_probability

    def make_move(self, game: a2_minichess.MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        if self._game_tree is not None and previous_move is not None:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)

        if self._game_tree is not None and self._game_tree.get_subtrees() != []:
            rand_float = random.uniform(0, 1)
            trees = self._game_tree.get_subtrees()
            if rand_float < self._exploration_probability:
                new_move = random.choice(game.get_valid_moves())
                if new_move not in [x.move for x in trees]:
                    self._game_tree = None
                return new_move
            # elif rand_float >= self._exploration_probability:
            else:
                white_wins = [x.white_win_probability for x in trees]
                if self._game_tree.is_white_move is True:
                    maximum = max(white_wins)
                    chosen = [x for x in trees if x.white_win_probability == maximum]
                    new1_move = chosen[0]
                    self._game_tree = new1_move
                    return new1_move.move
                else:
                    minimum = min(white_wins)
                    chosen = [x for x in trees if x.white_win_probability == minimum]
                    new1_move = chosen[0]
                    self._game_tree = new1_move
                    return new1_move.move
        else:
            new_move = random.choice(game.get_valid_moves())
            return new_move


def run_learning_algorithm(exploration_probabilities: list[float],
                           show_stats: bool = True) -> a2_game_tree.GameTree:
    """Play a sequence of Minichess games using an ExploringPlayer as the White player.

    This algorithm first initializes an empty GameTree. All ExploringPlayers will use this
    SAME GameTree object, which will be mutated over the course of the algorithm!
    Return this object.

    There are len(exploration_probabilities) games played, where at game i (starting at 0):
        - White is an ExploringPlayer (using the game tree) whose exploration probability
            is equal to exploration_probabilities[i]
        - Black is a RandomPlayer
        - AFTER the game, the move sequence from the game is inserted into the game tree,
          with a white win probability of 1.0 if White won the game, and 0.0 otherwise.

    Implementation note:
        - A NEW ExploringPlayer instance should be created for each loop iteration.
          However, each one should use the SAME GameTree object.
        - You should call run_game, NOT run_games, from a2_minichess. This is because you
          need more control over what happens after each game runs, which you can get by
          writing your own loop that calls run_game. However, you can base your loop on
          the implementation of run_games.
        - Note that run_game from a2_minichess returns both the winner and the move sequence
          after the game ends.
        - You may call print in this function to report progress made in each game.
        - Note that this function returns the final GameTree object. You can inspect the
          white_win_probability of its nodes, calculate its size, or and use it in a
          RandomTreePlayer or GreedyTreePlayer to see how they do with it.
    """
    # Start with a GameTree in the initial state
    game_tree = a2_game_tree.GameTree()

    # Play games using the ExploringPlayer and update the GameTree after each one
    results_so_far = []

    # Write your loop here, according to the description above.
    # for item in exploration_probabilities:
    for item in exploration_probabilities:
        white = ExploringPlayer(game_tree, item)
        black = a2_minichess.RandomPlayer()
        game = a2_minichess.run_game(white, black)
        results_so_far.append(game[0])
        if game[0] == 'White':
            probability = 1.0
        else:
            probability = 0.0
        game_tree.white_win_probability = probability
        game_tree.insert_move_sequence(game[1], probability)

    if show_stats:
        a2_minichess.plot_game_statistics(results_so_far)

    return game_tree


def decreasing(n: int) -> list[float]:
    """
    >>> decreasing(4)
    [1.0, 0.75, 0.5, 0.25, 0.0]
    >>> decreasing(8)
    [1.0, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0]
    """
    lst = []
    for i in range(n, -1, -1):
        lst.append(i / n)
    return lst


def nm_function(n: int, m: int) -> list[float]:
    """
    >>> nm_function (4, 5)
    [1.0, 0.75, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    """
    lst = decreasing(n)
    lst.extend([0.0] * m)
    return lst


def part3_runner() -> a2_game_tree.GameTree:
    """Run example for Part 3.

    Please note that unlike part1_runner and part2_runner, this function is NOT graded.
    We encourage you to experiment with different exploration probability sequences
    to see how quickly you can develop a "winning" GameTree!
    """
    probabilities = nm_function(500, 500)

    return run_learning_algorithm(probabilities)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4,
        'disable': ['E1136'],
        'extra-imports': ['random', 'a2_minichess', 'a2_game_tree'],
        'allowed-io': ['run_learning_algorithm']
    })

    part3_runner()
