classdef E01_ArraySum
    methods (Static)
        function total = arraySum(arr)
            % Sum all elements without using sum()
            % Hint: numel(arr), loop, accumulate
            total = 0;
            for i = 1:numel(arr)
                total = total + arr(i);
            end
        end
    end
end
