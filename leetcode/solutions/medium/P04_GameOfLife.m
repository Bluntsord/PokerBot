classdef P04_GameOfLife
    methods (Static)
        function nextGrid = gameOfLife(grid)
            [m, n] = size(grid);
            nextGrid = zeros(m, n);
            kernel = ones(3);
            neighbors = conv2(double(grid), kernel, 'same') - double(grid);
            for i = 1:m
                for j = 1:n
                    liveNeighbors = neighbors(i, j);
                    if grid(i, j) == 1
                        if liveNeighbors == 2 || liveNeighbors == 3
                            nextGrid(i, j) = 1;
                        end
                    else
                        if liveNeighbors == 3
                            nextGrid(i, j) = 1;
                        end
                    end
                end
            end
        end
    end
end
