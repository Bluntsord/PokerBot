classdef E06_CellBasics
    methods (Static)
        function result = cellBasics(C)
            result.firstNumber = [];
            result.firstString = '';
            result.allNumeric = [];
            foundNum = false; foundStr = false;
            nums = [];
            for k = 1:numel(C)
                val = C{k};
                if isnumeric(val)
                    nums = [nums, val(:)'];
                    if ~foundNum
                        result.firstNumber = val;
                        foundNum = true;
                    end
                elseif ischar(val) || isstring(val)
                    if ~foundStr
                        result.firstString = char(val);
                        foundStr = true;
                    end
                end
            end
            result.allNumeric = nums;
        end
    end
end
