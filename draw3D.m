%% Import data from spreadsheet
% Script for importing data from the following spreadsheet:
%
%    Workbook: D:\NTU\Ben50\Resistance Measurement.xlsx
%    Worksheet: 1201
%
% Auto-generated by MATLAB on 26-Dec-2022 14:40:46

% %% Setup the Import Options and import the data
% opts = spreadsheetImportOptions("NumVariables", 13);
% 
% % Specify sheet and range
% opts.Sheet = "1201";
% opts.DataRange = "A1:M185";
% 
% % Specify column names and types
% opts.VariableNames = ["length", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13"];
% opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];
% 
% % Import the data
% resT = readtable("D:\NTU\Ben50\Resistance Measurement.xlsx", opts, "UseExcel", false);
% res = table2array(resT);
% % disp(res);
% start_ = [2, 10, 24, 44, 70]; %, 102, 107, 118, 135, 158];
% end_ = [6, 18, 36, 60, 90]; %, 105, 116, 133, 156, 185];
% xx = [];
% yy = [];
% zz = [];
% for i = 1: 5
%     len = res(start_(i), 1);
%     for j = start_(i):end_(i)
%         for k = 2:11
%             xx = [xx; len];
%             yy = [yy; res(j, 1)/len];
%             zz = [zz; res(j, k)/res(start_(i),k)];
%         end
%     end
% end
% 
% [sf, gof] = fit([xx, yy], zz, 'poly23');
% p = plot(sf);
% alpha(p, 0.1);
% hold on;
% plot3(xx, yy, zz, '.', 'MarkerSize', 12);
% 
% %% Clear temporary variables
% clear opts
%% Setup the Import Options and import the data
opts = spreadsheetImportOptions("NumVariables", 13);

% Specify sheet and range
opts.Sheet = "stretch";
opts.DataRange = "A1:M185";

% Specify column names and types
opts.VariableNames = ["length", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Import the data
resT = readtable("D:\NTU\Ben50\newCord.xlsx", opts, "UseExcel", false);
res = table2array(resT);
% disp(res);
start_ = [2, 8, 18, 32, 50];
end_ = [6, 16, 30, 48, 70];
xx = [];
yy = [];
zz = [];
for i = 1: 5
    len = res(start_(i), 1);
    for j = start_(i):end_(i)
        for k = 2:11
            xx = [xx; len];
            yy = [yy; res(j, 1)/len];
            zz = [zz; res(j, k)];
        end
    end
end

[sf, gof] = fit([xx, yy], zz, 'poly23');
p = plot(sf);
alpha(p, 0.3);
hold on;
plot3(xx, yy, zz, '.', 'MarkerSize', 12);
hold off;
% legend("old", "new")
set (gca, 'xdir', 'reverse' )

%% Clear temporary variables
clear opts