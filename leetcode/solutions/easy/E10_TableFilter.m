classdef E10_TableFilter
    methods (Static)
        function [passed, failedNames] = filterTable(T, minScore)
            mask = T.Score >= minScore;
            passed = T(mask, :);
            failedNames = T.Name(~mask);
        end
    end
end
