classdef E07_SetMembership
    methods (Static)
        function [inBoth, onlyInA, isMember] = setOps(A, B)
            inBoth = sort(intersect(A, B));
            onlyInA = sort(setdiff(A, B));
            isMember = ismember(A, B);
        end
    end
end
