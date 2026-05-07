function result = runEasyTest(N)
    % runEasyTest      → all easy problems, YOUR solution (default)
    % runEasyTest(2)   → just E02, YOUR solution
    % runEasyTest('answer') → all easy, REFERENCE solution

    if nargin == 0
        targets = 1:11;
    elseif ischar(N) || isstring(N)
        if strcmp(N, 'answer')
            targets = 1:11;
        else
            targets = 1:11;
        end
    else
        targets = N;
    end

    useAnswer = nargin > 0 && ischar(N) && strcmp(N, 'answer');

    testRoot = fileparts(mfilename('fullpath'));
    if useAnswer
        addpath(fullfile(testRoot, '..', '..', 'solutions', 'easy'), '-begin');
    else
        addpath(fullfile(testRoot, '..', '..', 'user', 'easy'), '-begin');
    end
    rehash path;

    allPassed = true;
    for t = targets
        switch t
            case 1
                r = easyTestP01(); if ~r; allPassed = false; end
            case 2
                r = easyTestP02(); if ~r; allPassed = false; end
            case 3
                r = easyTestP03(); if ~r; allPassed = false; end
            case 4
                r = easyTestP04(); if ~r; allPassed = false; end
            case 5
                r = easyTestP05(); if ~r; allPassed = false; end
            case 6
                r = easyTestP06(); if ~r; allPassed = false; end
            case 7
                r = easyTestP07(); if ~r; allPassed = false; end
            case 8
                r = easyTestP08(); if ~r; allPassed = false; end
            case 9
                r = easyTestP09(); if ~r; allPassed = false; end
            case 10
                r = easyTestP10(); if ~r; allPassed = false; end
            case 11
                r = easyTestP11(); if ~r; allPassed = false; end
        end
    end

    fprintf('========================================\n');
    if allPassed
        fprintf('  ALL PASSED\n');
    else
        fprintf('  SOME FAILED\n');
    end
    fprintf('========================================\n');
    result = allPassed;
end

function p = easyTestP01()
    fprintf('--- E01: Array Sum ---\n');
    passed = 0; total = 0;
    tests = {
        {[1 2 3 4 5], 15}
        {[-1 0 3], 2}
        {7, 7}
        {[1 2; 3 4], 10}
    };
    for i = 1:length(tests)
        arr = tests{i}{1}; exp = tests{i}{2}; total = total + 1;
        try
            res = E01_ArraySum.arraySum(arr);
            if isequal(res, exp)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                Logger.writeLog(arr); Logger.writeLog(exp); Logger.writeLog(res);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP02()
    fprintf('--- E02: Find Max ---\n');
    passed = 0; total = 0;
    tests = {
        {[3 7 1 9 2], 9}
        {[-5 -2 -8], -2}
        {[10; 20; 5], 20}
        {42, 42}
    };
    for i = 1:length(tests)
        arr = tests{i}{1}; exp = tests{i}{2}; total = total + 1;
        try
            res = E02_FindMax.findMax(arr);
            if isequal(res, exp)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                Logger.writeLog(arr); Logger.writeLog(exp); Logger.writeLog(res);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP03()
    fprintf('--- E03: Count Where ---\n');
    passed = 0; total = 0;
    tests = {
        {[1 5 3 5 2], 3, 2, 1}
        {[10 20 30], 25, 1, 0}
        {7, 7, 0, 1}
        {[], 5, 0, 0}
    };
    for i = 1:length(tests)
        arr = tests{i}{1}; t = tests{i}{2};
        expG = tests{i}{3}; expE = tests{i}{4};
        total = total + 1;
        try
            [g, e] = E03_CountWhere.countWhere(arr, t);
            if isequal(g, expG) && isequal(e, expE)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED (exp g=%d e=%d, got g=%d e=%d)\n', i, expG, expE, g, e);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP04()
    fprintf('--- E04: Reverse Array ---\n');
    passed = 0; total = 0;
    tests = {
        {[1 2 3 4 5], [5 4 3 2 1]}
        {10, 10}
        {[1; 2; 3], [3; 2; 1]}
        {[], []}
    };
    for i = 1:length(tests)
        arr = tests{i}{1}; exp = tests{i}{2}; total = total + 1;
        try
            res = E04_ReverseArray.reverseArray(arr);
            if isequal(res, exp)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                Logger.writeLog(arr); Logger.writeLog(exp); Logger.writeLog(res);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP05()
    fprintf('--- E05: Dot Multiply ---\n');
    passed = 0; total = 0;
    tests = {
        {[1 2; 3 4], [5 6; 7 8], [5 12; 21 32]}
        {[1 2 3], [4 5 6], [4 10 18]}
        {10, 3, 30}
    };
    for i = 1:length(tests)
        A = tests{i}{1}; B = tests{i}{2}; exp = tests{i}{3}; total = total + 1;
        try
            res = E05_DotMultiply.dotMultiply(A, B);
            if isequal(res, exp)
                fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                Logger.writeLog(A, B); Logger.writeLog(exp); Logger.writeLog(res);
            end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    % Error case
    total = total + 1;
    try
        E05_DotMultiply.dotMultiply([1 2], [3 4 5]);
        fprintf('  %d. FAILED — should have thrown error\n', total);
    catch ME
        fprintf('  %d. PASSED (correctly threw error)\n', total); passed = passed + 1;
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP06()
    fprintf('--- E06: Cell Basics ---\n');
    passed = 0; total = 0;
    C = {42, 'hello', [1 2 3], 'world', 7};
    tests = {{C, 42, 'hello', [42 1 2 3 7]}};
    for i = 1:length(tests)
        C = tests{i}{1}; expNum = tests{i}{2}; expStr = tests{i}{3}; expAll = tests{i}{4};
        total = total + 1;
        try
            res = E06_CellBasics.cellBasics(C);
            ok = isequal(res.firstNumber, expNum) && isequal(res.firstString, expStr) && isequal(res.allNumeric, expAll);
            if ok; fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else fprintf('  %d. FAILED\n', i); end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP07()
    fprintf('--- E07: Set Membership ---\n');
    passed = 0; total = 0;
    A = [1 2 3 4 5]; B = [3 5 5 7 9];
    expBoth = [3 5]; expOnly = [1 2 4]; expMem = [false false true false true];
    tests = {{A, B}};
    for i = 1:length(tests)
        A = tests{i}{1}; B = tests{i}{2};
        total = total + 1;
        try
            [inBoth, onlyInA, isMember] = E07_SetMembership.setOps(A, B);
            ok = isequal(inBoth, expBoth) && isequal(onlyInA, expOnly) && isequal(isMember, expMem);
            if ok; fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else fprintf('  %d. FAILED\n', i); end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP08()
    fprintf('--- E08: Matrix Row/Col Ops ---\n');
    passed = 0; total = 0;
    M = [1 2 3; 4 5 6];
    tests = {{M, [6; 15], [4 5 6], [2; 5]}};
    for i = 1:length(tests)
        M = tests{i}{1}; expRS = tests{i}{2}; expCM = tests{i}{3}; expRM = tests{i}{4};
        total = total + 1;
        try
            [rowSums, colMaxes, rowMeans] = E08_MatrixStats.matrixStats(M);
            ok = isequal(rowSums, expRS) && isequal(colMaxes, expCM) && isequal(rowMeans, expRM);
            if ok; fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else fprintf('  %d. FAILED\n', i); end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP09()
    fprintf('--- E09: Table Basics ---\n');
    passed = 0; total = 0;
    names = {'Alice'; 'Bob'; 'Carol'};
    ages = [25; 30; 22];
    scores = [88; 92; 85];
    tests = {{names, ages, scores, 88.3333, 'Bob'}};
    for i = 1:length(tests)
        n = tests{i}{1}; a = tests{i}{2}; s = tests{i}{3};
        expAvg = tests{i}{4}; expOld = tests{i}{5};
        total = total + 1;
        try
            [T, avg, oldest] = E09_TableBasics.buildTable(n, a, s);
            ok = abs(avg - expAvg) < 0.001 && strcmp(oldest, expOld);
            if ok; fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else fprintf('  %d. FAILED (avg=%g oldest=%s)\n', i, avg, oldest); end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP10()
    fprintf('--- E10: Table Filter ---\n');
    passed = 0; total = 0;
    Name = {'A'; 'B'; 'C'; 'D'}; Score = [75; 45; 90; 55];
    T = table(Name, Score);
    tests = {{T, 60, {'A'; 'C'}, {'B'; 'D'}}};
    for i = 1:length(tests)
        Tbl = tests{i}{1}; thresh = tests{i}{2};
        expPassed = tests{i}{3}; expFailed = tests{i}{4};
        total = total + 1;
        try
            [passedTbl, failed] = E10_TableFilter.filterTable(Tbl, thresh);
            ok = isequal(passedTbl.Name, expPassed) && isequal(failed, expFailed);
            if ok; fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else fprintf('  %d. FAILED\n', i); end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end

function p = easyTestP11()
    fprintf('--- E11: Table GroupBy ---\n');
    passed = 0; total = 0;
    Dept = {'Eng'; 'Sales'; 'Eng'; 'Sales'; 'Mktg'};
    Salary = [100; 80; 120; 90; 70];
    T = table(Dept, Salary, 'VariableNames', {'Department', 'Salary'});
    tests = {{T, {'Eng'; 'Mktg'; 'Sales'}, [110; 70; 85], 'Eng'}};
    for i = 1:length(tests)
        Tbl = tests{i}{1}; expDepts = tests{i}{2};
        expAvgs = tests{i}{3}; expBest = tests{i}{4};
        total = total + 1;
        try
            [depts, avgs, best] = E11_TableGroupBy.groupByDepartment(Tbl);
            ok = isequal(depts, expDepts) && all(abs(avgs - expAvgs) < 0.001) && strcmp(best, expBest);
            if ok; fprintf('  %d. PASSED\n', i); passed = passed + 1;
            else fprintf('  %d. FAILED\n', i); end
        catch ME; fprintf('  %d. ERROR: %s\n', i, ME.message); end
    end
    p = (passed == total);
    fprintf('  Result: %d/%d\n\n', passed, total);
end
