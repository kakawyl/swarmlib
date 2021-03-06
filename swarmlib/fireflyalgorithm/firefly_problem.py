# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from copy import deepcopy
import logging

from .firefly import Firefly
from .visualizer import Visualizer
LOGGER = logging.getLogger(__name__)


class FireflyProblem():
    def __init__(self, **kwargs):
        """Initializes a new instance of the `FireflyProblem` class.

        Keyword arguments:  \r
        `firefly_number`   -- Number of fireflies used for solving
        `function`         -- The 2D evaluation function. Its input is a 2D numpy.array  \r
        `upper_boundary`   -- Upper boundary of the function (default 4)  \r
        `lower_boundary`   -- Lower boundary of the function (default 0)  \r
        `alpha`            -- Randomization parameter (default 0.25)  \r
        `beta`             -- Attractiveness at distance=0 (default 1)  \r
        `gamma`            -- Characterizes the variation of the attractiveness. (default 0.97) \r
        `iteration_number` -- Number of iterations to execute (default 100)  \r
        `interval`         -- Interval between two animation frames in ms (default 500)  \r
        `continuous`       -- Indicates whether the algorithm should run continuously (default False)
        """

        self.__iteration_number = kwargs.get('iteration_number', 10)
        # Create fireflies
        self.__fireflies = [
            Firefly(**kwargs)
            for _ in range(kwargs['firefly_number'])
        ]

        # Initialize intensity
        for firefly in self.__fireflies:
            firefly.update_intensity()

        # Initialize visualizer for plotting
        self.__visualizer = Visualizer(**kwargs)
        self.__visualizer.add_data(positions=[firefly.position for firefly in self.__fireflies])

    def solve(self):
        """Solve the problem."""
        best = None
        for _ in range(self.__iteration_number):
            for i in self.__fireflies:
                for j in self.__fireflies:
                    if j.value < i.value:
                        i.move_towards(j.position)
                        i.update_intensity()

            current_best = min(self.__fireflies, key=lambda firefly: firefly.value)
            if not best or current_best.value < best.value:
                best = deepcopy(current_best)

            LOGGER.info('Current best value: %s, Overall best value: %s', current_best.value, best.value)

            # randomly walk the best firefly
            current_best.random_walk(0.1)
            current_best.update_intensity()

            # Add data for visualization
            self.__visualizer.add_data(positions=[firefly.position for firefly in self.__fireflies])

        return best

    def replay(self):
        """Play the visualization"""
        self.__visualizer.replay()
