classdef P04_GameOfLife
    methods (Static)
        function nextGrid = gameOfLife(grid)
            % One step of Conway's Game of Life.
            % 1. Preallocate: nextGrid = zeros(size(grid))
            % 2. Count neighbors using conv2 or manual loops
            % 3. Apply the 4 rules with logical indexing
            nextGrid = zeros(size(grid));  % Replace this
        end
    end
end
