dt = 1;

figure1 = figure;
axes1 = axes('Parent',figure1);
hold(axes1,'on');

[X, Y, Z] = LoadSavedData('D:\Projects\VREP\python-20180326\tri_peg_hole_data\x15_z0-120\results2018-03-27-0623_port20004.csv');

num_x = size(tabulate(X), 1); % 统计有多少个不同的x值
num_y = size(tabulate(Y), 1);
if (num_x * num_y ~= length(X))
    error('Incomplete data file, please use plot=1 to draw the figure.');
end
X = reshape(X, num_x, num_y);
Y = reshape(Y, num_x, num_y);
Z = reshape(Z, num_x, num_y);

% resize
X = X(1:dt:end, 1:dt:end);
Y = Y(1:dt:end, 1:dt:end);
Z = Z(1:dt:end, 1:dt:end);
mesh(X, Y, Z,'Parent',axes1);

% 创建 label
xlabel('x','Interpreter','latex');
zlabel('z','Interpreter','latex');
ylabel('y','Interpreter','latex');

view(axes1,[-39.1 58.16]);
grid(axes1,'on');
% axis(axes1,'tight');
% % 设置其余坐标轴属性
% set(axes1,'DataAspectRatio',[1 1 1],'XTickLabel',{'','','','','',''},...
%     'YTickLabel',{'','','','','',''},'ZTickLabel',{'',''});

axis on;
axis([-0.015,0.015,-0.005,0.025,0.12,0.15]);
set(axes1,'DataAspectRatio',[1 1 1]);