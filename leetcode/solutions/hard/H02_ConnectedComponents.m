classdef H02_ConnectedComponents
    methods (Static)
        function [numComponents, labels] = connectedComponents(adj)
            n = size(adj, 1);
            labels = zeros(1, n);
            visited = false(1, n);
            compId = 0;
            for i = 1:n
                if ~visited(i)
                    compId = compId + 1;
                    stack = i;
                    while ~isempty(stack)
                        u = stack(end);
                        stack(end) = [];
                        if visited(u); continue; end
                        visited(u) = true;
                        labels(u) = compId;
                        for v = n:-1:1
                            if adj(u, v) == 1 && ~visited(v)
                                stack = [stack, v];
                            end
                        end
                    end
                end
            end
            numComponents = compId;
        end
    end
end
