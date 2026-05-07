classdef E11_TableGroupBy
    methods (Static)
        function [departments, avgSalaries, bestPaid] = groupByDepartment(T)
            departments = sort(unique(T.Department));
            avgSalaries = zeros(size(departments));
            for k = 1:length(departments)
                mask = ismember(T.Department, departments{k});
                avgSalaries(k) = mean(T.Salary(mask));
            end
            [~, idx] = max(avgSalaries);
            bestPaid = departments{idx};
        end
    end
end
