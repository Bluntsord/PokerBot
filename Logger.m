classdef Logger
    methods (Static)
        function writeLog(varargin)
            timestamp = ['[', datestr(now, 'HH:MM:SS'), ']'];
            if nargin == 0
                return;
            end
            if nargin >= 2 && ischar(varargin{1}) && contains(varargin{1}, '%')
                fprintf(['%s ', varargin{1}, '\n'], timestamp, varargin{2:end});
            else
                for k = 1:nargin
                    fprintf('%s Param %d: ', timestamp, k);
                    Logger.dispVal(varargin{k});
                end
            end
        end
    end
    methods (Static, Access = private)
        function dispVal(v)
            t = class(v);
            s = size(v);
            ds = Logger.dimstr(s);
            if isnumeric(v)
                if isscalar(v)
                    fprintf('Type: %-8s | Size: %-6s | Value: %g\n', t, ds, v);
                elseif isvector(v)
                    fprintf('Type: %-8s | Size: %-6s | Value: [%s]\n', t, ds, strjoin(cellstr(num2str(v(:)')), ' '));
                else
                    fprintf('Type: %-8s | Size: %-6s |\n', t, ds);
                    disp(v);
                end
            elseif islogical(v)
                if isscalar(v)
                    fprintf('Type: %-8s | Size: %-6s | Value: %s\n', t, ds, mat2str(v));
                elseif isvector(v)
                    fprintf('Type: %-8s | Size: %-6s | Value: [%s]\n', t, ds, strjoin(cellstr(num2str(v(:)')), ' '));
                else
                    fprintf('Type: %-8s | Size: %-6s |\n', t, ds);
                    disp(v);
                end
            elseif isstring(v)
                if isscalar(v)
                    fprintf('Type: %-8s | Size: %-6s | Value: "%s"\n', t, ds, v);
                else
                    fprintf('Type: %-8s | Size: %-6s |\n', t, ds);
                    disp(v);
                end
            elseif ischar(v)
                fprintf('Type: %-8s | Size: %-6s | Value: ''%s''\n', t, ds, v);
            elseif iscell(v)
                if isvector(v) && numel(v) <= 10
                    parts = {};
                    for k = 1:numel(v)
                        if isnumeric(v{k}) || islogical(v{k})
                            parts{end+1} = num2str(v{k});
                        else
                            parts{end+1} = class(v{k});
                        end
                    end
                    fprintf('Type: %-8s | Size: %-6s | Value: {%s}\n', t, ds, strjoin(parts, ', '));
                else
                    fprintf('Type: %-8s | Size: %-6s |\n', t, ds);
                    disp(v);
                end
            elseif isstruct(v)
                fprintf('Type: %-8s | Size: %-6s | Fields: %s\n', t, ds, strjoin(fieldnames(v), ', '));
            elseif isa(v, 'containers.Map')
                fprintf('Type: %-8s | Size: %-6s | Keys: %d\n', t, ds, v.Count);
            else
                fprintf('Type: %-8s | Size: %-6s |\n', t, ds);
                disp(v);
            end
        end
        function s = dimstr(sz)
            if isempty(sz) || prod(sz) == 0
                s = '0';
            else
                s = strjoin(arrayfun(@num2str, sz(:)', 'UniformOutput', false), 'x');
            end
        end
    end
end
