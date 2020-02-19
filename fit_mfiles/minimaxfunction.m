%fitting a function to minimax plots
%for three states A,B, and C 
depth_cutoffs = [3; 4; 5; 6; 3; 4; 5; 6; 3; 4; 5; 6];
num_states_explored = [1824; 30227; 357942; 5880018; 3562; 47777; 759695; 10535941; 3079; 47792; 714876; 11356159];
f = fit(depth_cutoffs,num_states_explored,'exp1');
f
h=plot(f,'r',depth_cutoffs,num_states_explored,'r.')
set(h,'MarkerSize',15);

% Annotations
xlabel('Depth cutoff');
ylabel('Number of states explored');

legend('show');
legend('Data points','Fitted curve','location','southwest');
lgd = legend;
lgd.Location = 'southwest';

grid on;