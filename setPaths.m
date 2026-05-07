function setPaths()
    root = fileparts(mfilename('fullpath'));
    addpath(genpath(root));
    fprintf('Added %s and all subdirectories to the MATLAB path.\n', root);
end
