classdef E03_CountWhere
    methods (Static)
        function [countGreater, countEqual] = countWhere(arr, t)
            countGreater = 0;
            countEqual = 0;
            for k = 1:numel(arr)
                if arr(k) > t
                    countGreater = countGreater + 1;
                elseif arr(k) == t
                    countEqual = countEqual + 1;
                end
            end
        end
    end
end
