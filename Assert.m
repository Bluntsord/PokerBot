classdef Assert
    methods (Static)
        function assertEquals(expected, actual)
            if ~isequal(actual, expected)
                error('Assertion failed.\nExpected: %s\nActual:   %s', ...
                    mat2str(expected), mat2str(actual));
            end
        end
    end
end
