function result = runTestP04(varargin)
    [runAll, useAnswer, targetCase] = parseArgs(varargin{:});

    if useAnswer
        addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'solutions', 'medium'), '-begin');
    else
        addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'user', 'medium'), '-begin');
    end
    rehash path;

    fprintf('--- P04: Game of Life ---\n');
    passed = 0; total = 0;

    blinkerIn  = zeros(5);      blinkerIn(3, 2:4) = 1;
    blinkerOut = zeros(5);      blinkerOut(2:4, 3) = 1;
    block = [1 1; 1 1];
    single = zeros(3); single(2,2) = 1;

    testCases = {
        {blinkerIn, blinkerOut},
        {block, block},
        {single, zeros(3)},
        {zeros(4), zeros(4)},
    };

    startIdx = 1; endIdx = 1;
    if ~isnan(targetCase); startIdx = targetCase; endIdx = targetCase;
    elseif runAll; endIdx = length(testCases); end
    if targetCase > length(testCases); startIdx = length(testCases)+1; endIdx = length(testCases)+1; end

    for i = startIdx:min(endIdx, length(testCases))
        input = testCases{i}{1}; expected = testCases{i}{2};
        total = total + 1;
        try
            res = P04_GameOfLife.gameOfLife(input);
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
