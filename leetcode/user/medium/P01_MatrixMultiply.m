classdef P01_MatrixMultiply
    methods (Static)
        function C = multiply(A, B)
            % Multiply A (m*k) by B (k*n), return C (m*n). No A*B allowed.
            % 1. Check dimensions match: size(A,2) == size(B,1)
            % 2. Preallocate: C = zeros(m, n)
            % 3. Triple nested loop: i over rows, j over cols, p over inner
            Assert.assertEquals(width(A),height(B));
            l = Logger();
            C = zeros(height(A), width(B));
            for a_rows = 1:height(A)
                for b_col = 1: width(B)
                    C(a_rows, b_col) = sum(A(a_rows, :) .* B(:,b_col)');
                end
            end
        end
    end
end
