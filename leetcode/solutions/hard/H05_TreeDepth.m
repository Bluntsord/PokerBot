classdef H05_TreeDepth
    methods (Static)
        function d = maxDepth(root)
            if isempty(root)
                d = 0;
                return;
            end
            d = 1 + max(H05_TreeDepth.maxDepth(root.left), H05_TreeDepth.maxDepth(root.right));
        end
    end
end
