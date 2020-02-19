%fitting a function to minimax + alpha-beta pruning plots
%for three states A,B, and C   
depth_cutoffs = [3; 4; 5; 6; 3; 4; 5; 6; 3; 4; 5; 6];
num_states_explored = [546; 3622; 23423; 214603; 640; 1056; 10367; 29879; 497; 2391; 19246; 54097];
f = fit(depth_cutoffs,num_states_explored,'exp1');
f
h=plot(f,'b',depth_cutoffs,num_states_explored,'b.')
set(h,'MarkerSize',15);

% Annotations
xlabel('Depth cutoff');
ylabel('Number of states explored');

legend('show');
legend('Data points','Fitted curve','location','southwest');
lgd = legend;
lgd.Location = 'southwest';

grid on;