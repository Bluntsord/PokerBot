% Define Test Cases: {nums, target, expected_indices}
testCases = {
  {[2, 7, 11, 15], 9, [1, 2]},           % Standard case
  {[3, 2, 4], 6, [2, 3]},                % Indices are not the first element
  {[3, 3], 6, [1, 2]},                   % Duplicate values
  {[-1, -2, -3, -4, -5], -8, [3, 5]},    % Negative numbers
  {[0, 4, 3, 0], 0, [1, 4]},             % Multiple zeros
  {[10, 20, 30, 40, 50], 90, [4, 5]},    % Larger numbers at the end
  {[1, 5, 8, 12, 19], 20, [3, 4]},       % Target is sum of middle elements
  {[-10, 7, 2, 15], 5, [1, 4]},          % Mixed positive and negative
  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19, [9, 10]}, % Larger array
  {[100, 200, 300], 400, [1, 3]}         % Wide gap between indices
  };

fprintf('Running TwoSum Test Suite...\n');
fprintf('---------------------------------\n');

passCount = 0;

for i = 1:length(testCases)
  nums = testCases{i}{1};
  target = testCases{i}{2};
  expected = testCases{i}{3};

  % Call your class method
  try
    result = TwoSum.solution(nums, target);

    % Sort results to ensure order doesn't cause a false failure
    if isequal(sort(result), sort(expected))
      fprintf('Test Case %d: PASSED\n', i);
      passCount = passCount + 1;
    else
      fprintf('Test Case %d: FAILED (Expected [%s], got [%s])\n', ...
        i, num2str(expected), num2str(result));
    end
  catch ME
    fprintf('Test Case %d: ERROR (%s)\n', i, ME.message);
  end
end

fprintf('---------------------------------\n');
fprintf('Final Result: %d/%d tests passed.\n', passCount, length(testCases));
