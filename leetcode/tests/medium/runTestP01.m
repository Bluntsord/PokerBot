function result = runTestP01(varargin)
    % runTestP01          → first test case, your solution
    % runTestP01(3)       → test case 3 only
    % runTestP01('all')   → all test cases
    % runTestP01('answer') → first case, reference solution

    [runAll, useAnswer, targetCase] = parseArgs(varargin{:});

    if useAnswer
        addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'solutions', 'medium'), '-begin');
    else
        addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'user', 'medium'), '-begin');
    end
    rehash path;

    fprintf('--- P01: Matrix Multiplication ---\n');
    passed = 0; total = 0;

    testCases = {
        {[2 1 3; 0 4 2; 1 0 5], [1 0 2; 3 2 1; 0 4 1], [5 14 8; 12 16 6; 1 20 7]},
        {[1 2; 3 4], [5 6; 7 8], [19 22; 43 50]},
        {[1 0; 2 1; 0 3], [1 2 3; 0 1 1], [1 2 3; 2 5 7; 0 3 3]},
        {[4 2 1; 3 5 6], eye(3), [4 2 1; 3 5 6]},
        {[1 2 3], [4; 5; 6], 32},
    };
    errorCaseNum = length(testCases) + 1;

    startIdx = 1; endIdx = 1;
    if ~isnan(targetCase); startIdx = targetCase; endIdx = targetCase;
    elseif runAll; endIdx = length(testCases); end
    if targetCase > length(testCases); startIdx = length(testCases) + 1; endIdx = length(testCases) + 1; end

    for i = startIdx:min(endIdx, length(testCases))
        A = testCases{i}{1}; B = testCases{i}{2}; expected = testCases{i}{3};
        total = total + 1;
        try
            res = P01_MatrixMultiply.multiply(A, B);
            if isequal(res, expected)
                fprintf('  %d. PASSED\n', i);
                passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                fprintf('\n========== Inputs =============\n');
                Logger.writeLog(A, B);
                fprintf('========== Expected ==========\n');
                Logger.writeLog(expected);
                fprintf('========== Your Answer ========\n');
                Logger.writeLog(res);
            end
        catch ME
            fprintf('  %d. ERROR: %s\n', i, ME.message);
        end
    end

    if (runAll || targetCase == errorCaseNum)
        total = total + 1;
        fprintf('  %d. ', errorCaseNum);
        try
            P01_MatrixMultiply.multiply([1 2; 3 4], [1 2 3]);
            fprintf('FAILED — should have thrown error\n');
            Logger.writeLog([1 2; 3 4], [1 2 3]);
        catch ME
            fprintf('PASSED (correctly threw error)\n');
            passed = passed + 1;
        end
    end

    result = (passed == total);
    fprintf('  Result: %d/%d passed\n\n', passed, total);
end

function [runAll, useAnswer, targetCase] = parseArgs(varargin)
    runAll = false; useAnswer = false; targetCase = NaN;
    for k = 1:nargin
        arg = varargin{k};
        if ischar(arg) || isstring(arg)
            if strcmp(arg, 'all'); runAll = true;
            elseif strcmp(arg, 'answer'); useAnswer = true;
            end
        elseif isnumeric(arg)
            targetCase = arg(1);
        end
    end
end
