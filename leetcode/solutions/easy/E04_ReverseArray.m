classdef E04_ReverseArray
    methods (Static)
        function result = reverseArray(arr)
            n = numel(arr);
            result = zeros(size(arr));
            for i = 1:n
                result(i) = arr(n - i + 1);
            end
        end
    end
end
