classdef H03_Fibonacci
    methods (Static)
        function result = fibonacci(n)
            persistent cache;
            if isempty(cache)
                cache = containers.Map('KeyType', 'double', 'ValueType', 'double');
            end
            if n <= 0
                error('n must be positive');
            end
            if n == 1 || n == 2
                result = 1;
                return;
            end
            if isKey(cache, n)
                result = cache(n);
                return;
            end
            result = H03_Fibonacci.fibonacci(n-1) + H03_Fibonacci.fibonacci(n-2);
            cache(n) = result;
        end
    end
end
