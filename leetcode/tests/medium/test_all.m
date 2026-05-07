function test_all(varargin)
    % test_all         → tests YOUR solutions (default)
    % test_all('answer') → tests REFERENCE solutions

    fprintf('========================================\n');
    fprintf('  LeetCode MATLAB Test Suite\n');

    testRoot = fileparts(mfilename('fullpath'));
    leetcodeDir = fullfile(testRoot, '..', '..');

    if nargin > 0 && strcmp(varargin{1}, 'answer')
        addpath(fullfile(leetcodeDir, 'solutions', 'medium'), '-begin');
        rehash path;
        fprintf('  Testing REFERENCE solutions (medium)\n');
    else
        addpath(fullfile(leetcodeDir, 'user', 'medium'), '-begin');
        rehash path;
        fprintf('  Testing YOUR solutions (medium)\n');
    end
    fprintf('========================================\n\n');

    r1 = runTestP01();
    r2 = runTestP02();
    r3 = runTestP03();
    r4 = runTestP04();

    allPassed = r1 && r2 && r3 && r4;
    fprintf('========================================\n');
    if allPassed
        fprintf('  ALL TESTS PASSED\n');
    else
        fprintf('  SOME TESTS FAILED\n');
    end
    fprintf('========================================\n');
end
