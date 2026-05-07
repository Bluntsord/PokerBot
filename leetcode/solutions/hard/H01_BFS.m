classdef H01_BFS
    methods (Static)
        function [order, distances] = bfs(adj, s)
            n = size(adj, 1);
            visited = false(1, n);
            distances = inf(1, n);
            order = [];
            queue = s;
            visited(s) = true;
            distances(s) = 0;
            while ~isempty(queue)
                u = queue(1);
                queue(1) = [];
                order = [order, u];
                for v = 1:n
                    if adj(u, v) == 1 && ~visited(v)
                        visited(v) = true;
                        distances(v) = distances(u) + 1;
                        queue = [queue, v];
                    end
                end
            end
        end
    end
end
