% Simple Alpha Test: SMA Crossover
prices = [100, 102, 101, 105, 107, 110, 108, 112, 115, 120];
short_sma = movmean(prices, 3);
long_sma = movmean(prices, 5);

fprintf('--- Backtest Results ---\n');
for i = 1:length(prices)
  if short_sma(i) > long_sma(i)
    fprintf('Day %d: Signal: BUY  | Price: %.2f\n', i, prices(i));
  else
    fprintf('Day %d: Signal: HOLD | Price: %.2f\n', i, prices(i));
  end
end

% Test plotting (this will open a window on your Mac)
plot(prices, '-o', 'LineWidth', 2); hold on;
plot(short_sma, '--', 'LineWidth', 1.5);
legend('Price', '3-Day SMA');
title('Momentum Test');
