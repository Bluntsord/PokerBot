classdef P01_MatrixMultiply
    methods (Static)
        function C = multiply(A, B)
            [m, kA] = size(A);
            [kB, n] = size(B);
            if kA ~= kB
                error('Inner dimensions must match: A is %dx%d, B is %dx%d', m, kA, kB, n);
            end
            C = zeros(m, n);
            for i = 1:m
                for j = 1:n
                    for p = 1:kA
                        C(i, j) = C(i, j) + A(i, p) * B(p, j);
                    end
                end
            end
        end
    end
end
