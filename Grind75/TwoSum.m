classdef TwoSum
  methods (Static)
    function indices = solution(nums, target)
      map = containers.Map('KeyType', 'double', 'ValueType', 'double');
      for i = 1:length(nums)
        complement = target - nums(i);
        if isKey(map, complement)
          indices = [map(complement), i];
          return;
        end
        map(nums(i)) = i;
      end
      indices = [];
    end
  end
end
