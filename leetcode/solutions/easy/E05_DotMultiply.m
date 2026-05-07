classdef E05_DotMultiply
    methods (Static)
        function C = dotMultiply(A, B)
            if ~isequal(size(A), size(B))
                error('Arrays must have the same size');
            end
            C = zeros(size(A));
            for k = 1:numel(A)
                C(k) = A(k) * B(k);
            end
        end
    end
end
