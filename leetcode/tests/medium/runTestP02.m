function result = runTestP02(varargin)
    [runAll, useAnswer, targetCase] = parseArgs(varargin{:});

    if useAnswer
        addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'solutions', 'medium'), '-begin');
    else
        addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'user', 'medium'), '-begin');
    end
    rehash path;

    fprintf('--- P02: Rotate Image ---\n');
    passed = 0; total = 0;

    testCases = {
        {[1 2 3; 4 5 6; 7 8 9], [7 4 1; 8 5 2; 9 6 3]},
        {[1 2; 3 4], [3 1; 4 2]},
        {42, 42},
    };
    errorCaseNum = length(testCases) + 1;

    startIdx = 1; endIdx = 1;
    if ~isnan(targetCase); startIdx = targetCase; endIdx = targetCase;
    elseif runAll; endIdx = length(testCases); end
    if targetCase > length(testCases); startIdx = length(testCases)+1; endIdx = length(testCases)+1; end

    for i = startIdx:min(endIdx, length(testCases))
        input = testCases{i}{1}; expected = testCases{i}{2};
        total = total + 1;
        try
            res = P02_RotateImage.rotate(input);
            if isequal(res, expected)
                fprintf('  %d. PASSED\n', i);
                passed = passed + 1;
            else
                fprintf('  %d. FAILED\n', i);
                fprintf('\n========== Input ==============\n');
                Logger.writeLog(input);
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
            P02_RotateImage.rotate([1 2 3; 4 5 6]);
            fprintf('FAILED — should have thrown error\n');
            Logger.writeLog([1 2 3; 4 5 6]);
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
