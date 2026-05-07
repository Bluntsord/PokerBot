classdef E02_FindMax
    methods (Static)
        function m = findMax(arr)
            m = arr(1);
            for k = 2:numel(arr)
                if arr(k) > m
                    m = arr(k);
                end
            end
        end
    end
end
