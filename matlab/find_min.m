% fileFolder='D:\Projects\VREP\python-20180326\tri_peg_hole_data\x20_z0-120\';%�ļ�����plane
fileFolder='D:\Projects\VREP\python-20180326\rec_peg_hole_data\x20_z0-90\';
is_plot = 0;

dirOutput=dir(fullfile(fileFolder,'*.csv'));%������ڲ�ͬ���͵��ļ����á�*����ȡ���У������ȡ�ض������ļ���'.'�����ļ����ͣ������á�.jpg��
fileNames={dirOutput.name}';

dt = 1;
x_angles = [10, 15, 20];
z_angles = 0:5:85;

x_cons = [-0.025, 0.03];
y_cons = [-0.01, 0.03];

d_min = zeros(1, length(z_angles));

for i=1:length(z_angles)
    [X, Y, Z] =  LoadSavedData([fileFolder fileNames{i}]);
    
    num_x = size(tabulate(X), 1); % ͳ���ж��ٸ���ͬ��xֵ
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
    
    % ȥ���߽����ر�С��ֵ
    X_idx = (X <= x_cons(1)) | (X >= x_cons(2));
    Z(X_idx) = Inf;
    Y_idx = (Y <= y_cons(1)) | (Y >= y_cons(2));
    Z(Y_idx) = Inf;
    
    d_min(i) = min(min(Z));
    
    if (is_plot == 1)
        figure;
        mesh(X, Y, Z);
        view(0, 90);
        % ���� label
        xlabel('x','Interpreter','latex');
        zlabel('z','Interpreter','latex');
        ylabel('y','Interpreter','latex');
    end
end

figure;
plot(z_angles, d_min);
