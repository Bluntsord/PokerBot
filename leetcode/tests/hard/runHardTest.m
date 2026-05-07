function result = runHardTest(N)
    % runHardTest      → all hard problems, YOUR solution
    % runHardTest(2)   → just H02
    % runHardTest('answer') → reference solutions

    if nargin == 0
        targets = 1:5;
    elseif ischar(N) || isstring(N)
        targets = 1:5;
    else
        targets = N;
    end

    useAnswer = nargin > 0 && ischar(N) && strcmp(N, 'answer');
    testRoot = fileparts(mfilename('fullpath'));
    if useAnswer
        addpath(fullfile(testRoot, '..', '..', 'solutions', 'hard'), '-begin');
    else
        addpath(fullfile(testRoot, '..', '..', 'user', 'hard'), '-begin');
    end
    rehash path;

    allPassed = true;
    for t = targets
        switch t
            case 1; r = testH01(); if ~r; allPassed = false; end
            case 2; r = testH02(); if ~r; allPassed = false; end
            case 3; r = testH03(); if ~r; allPassed = false; end
            case 4; r = testH04(); if ~r; allPassed = false; end
            case 5; r = testH05(); if ~r; allPassed = false; end
        end
    end
    fprintf('========================================\n');
    if allPassed; fprintf('  ALL PASSED\n'); else fprintf('  SOME FAILED\n'); end
    fprintf('========================================\n');
    result = allPassed;
end

function p = testH01()
    fprintf('--- H01: BFS ---\n');
    passed = 0; total = 0;
    adj = [0 1 1 0; 0 0 0 1; 0 0 0 1; 0 0 0 0];
    tests = {{adj, 1, [1 2 3 4], [0 1 1 2]}};
    for i = 1:length(tests)
        A = tests{i}{1}; s = tests{i}{2}; expOrd = tests{i}{3}; expDist = tests{i}{4};
        total = total + 1;
        try
            [ord, dist] = H01_BFS.bfs(A, s);
            if isequal(ord, expOrd) && isequal(dist, expDist)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                Logger.writeLog(ord, dist);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = testH02()
    fprintf('--- H02: Connected Components ---\n');
    passed = 0; total = 0;
    adj = [0 1 0 0 0; 1 0 0 0 0; 0 0 0 1 1; 0 0 1 0 1; 0 0 1 1 0];
    tests = {{adj, 2, [1 1 2 2 2]}};
    for i = 1:length(tests)
        A = tests{i}{1}; expNum = tests{i}{2}; expLabs = tests{i}{3};
        total = total + 1;
        try
            [num, labs] = H02_ConnectedComponents.connectedComponents(A);
            if num == expNum && isequal(labs, expLabs)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED (num=%d labs=%s)\n', i, num, mat2str(labs));
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = testH03()
    fprintf('--- H03: Fibonacci DP ---\n');
    passed = 0; total = 0;
    tests = {1, 1; 2, 1; 10, 55; 20, 6765};
    for i = 1:size(tests, 1)
        n = tests{i, 1}; exp = tests{i, 2};
        total = total + 1;
        try
            res = H03_Fibonacci.fibonacci(n);
            if res == exp
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED (n=%d got %d)\n', i, n, res);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = testH04()
    fprintf('--- H04: Longest Increasing Subseq ---\n');
    passed = 0; total = 0;
    tests = {
        {[10 9 2 5 3 7 101 18], 4}
        {[3 3 3], 1}
        {[1 2 3 4 5], 5}
        {[5], 1}
        {[], 0}
    };
    for i = 1:length(tests)
        arr = tests{i}{1}; exp = tests{i}{2};
        total = total + 1;
        try
            res = H04_LIS.longestIncreasingSubsequence(arr);
            if res == exp
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED (got %d, exp %d)\n', i, res, exp);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = testH05()
    fprintf('--- H05: Tree Max Depth ---\n');
    passed = 0; total = 0;
    root1 = struct('val', 1, 'left', [], 'right', []);
    root2 = struct('val', 1, ...
        'left',  struct('val', 2, ...
            'left', struct('val', 4, 'left', [], 'right', []), 'right', []), ...
        'right', struct('val', 3, 'left', [], 'right', []));
    tests = {{root1, 1}, {root2, 3}, {[], 0}};
    for i = 1:length(tests)
        r = tests{i}{1}; exp = tests{i}{2};
        total = total + 1;
        try
            res = H05_TreeDepth.maxDepth(r);
            if res == exp
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED (got %d, exp %d)\n', i, res, exp);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end
