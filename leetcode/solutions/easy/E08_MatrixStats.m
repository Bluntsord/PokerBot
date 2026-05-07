classdef E08_MatrixStats
    methods (Static)
        function [rowSums, colMaxes, rowMeans] = matrixStats(M)
            m = size(M, 1);
            n = size(M, 2);
            rowSums = zeros(m, 1);
            colMaxes = zeros(1, n);
            rowMeans = zeros(m, 1);
            for i = 1:m
                rowSums(i) = sum(M(i, :));
                rowMeans(i) = mean(M(i, :));
            end
            for j = 1:n
                colMaxes(j) = max(M(:, j));
            end
        end
    end
end
