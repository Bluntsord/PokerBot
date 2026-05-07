classdef E09_TableBasics
    methods (Static)
        function [T, averageScore, oldestName] = buildTable(names, ages, scores)
            T = table(names(:), ages(:), scores(:), ...
                'VariableNames', {'Name', 'Age', 'Score'});
            averageScore = mean(T.Score);
            oldestName = T.Name{T.Age == max(T.Age)};
            if iscell(oldestName); oldestName = oldestName{1}; end
        end
    end
end
