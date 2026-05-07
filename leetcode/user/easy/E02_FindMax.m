classdef E02_FindMax
    methods (Static)
        function m = findMax(arr)
            % Find the max element without using max()
            % Hint: start with arr(1), then loop and compare
            m = arr(1)
            for i = 1:numel(arr)
                if arr(i) > m
                    m = arr(i);
                end 
            end
        end
    end
end
