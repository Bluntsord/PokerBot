classdef E10_TableFilter
    methods (Static)
        function [passed, failedNames] = filterTable(T, minScore)
            % Hint: T.Score >= minScore gives logical mask, T(mask, :)
            passed = [];
            failedNames = {};
        end
    end
end
