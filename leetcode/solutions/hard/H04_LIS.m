classdef H04_LIS
    methods (Static)
        function maxLen = longestIncreasingSubsequence(arr)
            n = length(arr);
            if n == 0
                maxLen = 0;
                return;
            end
            dp = ones(1, n);
            for i = 2:n
                for j = 1:i-1
                    if arr(j) < arr(i)
                        dp(i) = max(dp(i), dp(j) + 1);
                    end
                end
            end
            maxLen = max(dp);
        end
    end
end
