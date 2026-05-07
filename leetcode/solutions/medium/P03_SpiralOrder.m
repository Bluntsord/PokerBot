classdef P03_SpiralOrder
    methods (Static)
        function result = spiralOrder(matrix)
            if isempty(matrix)
                result = [];
                return;
            end
            [m, n] = size(matrix);
            result = zeros(1, m * n);
            top = 1; bottom = m; left = 1; right = n;
            idx = 1;
            while top <= bottom && left <= right
                for j = left:right
                    result(idx) = matrix(top, j);
                    idx = idx + 1;
                end
                top = top + 1;
                for i = top:bottom
                    result(idx) = matrix(i, right);
                    idx = idx + 1;
                end
                right = right - 1;
                if top <= bottom
                    for j = right:-1:left
                        result(idx) = matrix(bottom, j);
                        idx = idx + 1;
                    end
                    bottom = bottom - 1;
                end
                if left <= right
                    for i = bottom:-1:top
                        result(idx) = matrix(i, left);
                        idx = idx + 1;
                    end
                    left = left + 1;
                end
            end
        end
    end
end
