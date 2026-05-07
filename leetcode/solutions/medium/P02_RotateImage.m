classdef P02_RotateImage
    methods (Static)
        function matrix = rotate(matrix)
            [m, n] = size(matrix);
            if m ~= n
                error('Matrix must be square');
            end
            for i = 1:n
                for j = i+1:n
                    tmp = matrix(i, j);
                    matrix(i, j) = matrix(j, i);
                    matrix(j, i) = tmp;
                end
            end
            for i = 1:n
                matrix(i, :) = fliplr(matrix(i, :));
            end
        end
    end
end
