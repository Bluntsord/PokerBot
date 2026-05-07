classdef P02_RotateImage
    methods (Static)
        function matrix = rotate(matrix)
            % Rotate an n*n matrix 90 deg clockwise IN-PLACE.
            % 1. Check matrix is square, else error
            % 2. Transpose across diagonal, then flip each row left-right
            % Hint: matrix(i,j) <-> matrix(j,i) to transpose
            % Hint: fliplr(matrix(i,:)) to flip a row
        end
    end
end
