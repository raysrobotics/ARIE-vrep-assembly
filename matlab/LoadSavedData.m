function [x, y, z] = LoadSavedData(filename, plot)
% Load saved .csv file into workspace and plot the data points in figure
% Input:
%   filename - file name and path of the .csv file (format for each line: 
%              %f, %f, %f)
%   plot     - 0: do not plot the data in figure (default); 1: plot the
%              data in figure
%

if (nargin == 1)
    plot = 0;
end

% ��ʼ��������
delimiter = ',';
formatSpec = '%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');

% ���ݸ�ʽ��ȡ�����С�
% �õ��û������ɴ˴������õ��ļ��Ľṹ����������ļ����ִ����볢��ͨ�����빤���������ɴ��롣
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN, 'ReturnOnError', false);

% �ر��ı��ļ���
fclose(fileID);

% ����������������б�������
x = dataArray{:, 1};
y = dataArray{:, 2};
z = dataArray{:, 3};

switch(plot)
    case 1
        % plot3(x, y, z, '.')
        frgb = (z-min(z))/(max(z)-min(z));
        for i=1:length(frgb)
            plot3(x(i), y(i), z(i), 'Marker', '.', 'LineStyle', 'none', 'Color', [frgb(i), 1-frgb(i), 0]); hold on
        end
        xlabel('x');ylabel('y');zlabel('z');
        axis equal
    case 2
        % ����
        num_x = size(tabulate(x), 1); % ͳ���ж��ٸ���ͬ��xֵ
        num_y = size(tabulate(y), 1);
        if (num_x * num_y ~= length(x))
            error('Incomplete data file, please use plot=1 to draw the figure.');
        end
        
        X = reshape(x, num_x, num_y);
        Y = reshape(y, num_x, num_y);
        Z = reshape(z, num_x, num_y);
        
        mesh(X, Y, Z);
        xlabel('x');ylabel('y');zlabel('z');
        axis equal
    otherwise    
end