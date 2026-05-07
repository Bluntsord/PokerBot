classdef E06_CellBasics
    methods (Static)
        function result = cellBasics(C)
            % C is a cell array with mixed types. Return struct with:
            %   result.firstNumber — first numeric element
            %   result.firstString — first char/string
            %   result.allNumeric  — all numeric elements concatenated
            % Hint: loop + isnumeric(val), char(val), C{k}
            result.firstNumber = [];
            result.firstString = '';
            result.allNumeric = [];
        end
    end
end
