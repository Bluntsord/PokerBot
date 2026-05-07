classdef E01_ArraySum
    methods (Static)
        function total = arraySum(arr)
            total = 0;
            n = numel(arr);
            for k = 1:n
                total = total + arr(k);
            end
        end
    end
end
