clear;
clc;
close all

elev_data = load('elev.mat');
lat_data = load('lat.mat');
lon_data = load('lon.mat');
elev = cell2mat(struct2cell(elev_data))/3.281; % convert feet to meters
lat = cell2mat(struct2cell(lat_data));
lon = cell2mat(struct2cell(lon_data));

figure;
surf(lat,lon,elev);
colorbar
hold on
xlabel('Latitude');
ylabel('Longitude');
zlabel('Elevation');


% plot slice as plane
desired_lat = 42;
%desired_lon = 105.5;
%desired_lat = 42;
[~,ind] = min( abs( lat(:,1)-desired_lat ) );


slice = elev(ind,:);
new_h = smoothdata(slice,'gaussian',1);


figure;


subplot(2,1,1);
hold on
plot(lon(1,:),slice,'black','LineWidth',2);
plot(lon(1,:),new_h,'black','LineWidth',2);
a = area(lon(1,:),new_h,1000);
a.FaceColor = 'black';
a.FaceAlpha = 0.3;
title(['Topography at latitude = ', num2str(lat(ind,1))]);
xlabel('Longitude');
ylabel('Elevation');
set(gca,'TickLength',[0.02, 0.05]);
set(gca,'LineWidth',1);
box on

%legend('true data','smoothed data');

ax = gca;
ax.FontSize = 15;


N = size(new_h,2);

xspan = lon(1,:);
%h = exp(-((xspan-1)/.1).^2)/2;
%h = -exp(-((xspan-1/2)/.1).^2)/2 + exp(-(xspan/.1).^2)/2;
h = new_h;
dh = gradient(h)./gradient(xspan);
g = 9.8;


%% ode45 (Runge-Kutta)


D1 = 10000/3.281; % subcritical

uvals = [100 120 140];
Fr_init = uvals.^2/(g*D1);

% plot Froude number on separate vertical axis

subplot(2,1,2);
hold on
%plot(xspan,h,'LineWidth',2);

for j=1:size(uvals,2)
    u1 = uvals(j);


    %[xspan,y] = ode45(@(x,y) fun(x,y,xspan,dh,g), xspan, [u1; D1]);
    [xspan,y] = ode45(@(x,y) fun2(x,y,xspan,dh,g,u1,D1), xspan, u1);
%     
%     u = y(:,1);
%     D = y(:,2);

    u = y;
    D = u1*D1./y;
    Fr = u.^2./(g*D);


    %hold on
    
    %subplot(3,2,j);
    %plot(xspan,D+h','LineWidth',2);
%     ind1 = find(Fr < 1);
%     ind2 = find(Fr >= 1);
%     plot(xspan(ind1),u(ind1),'blue','LineWidth',2);
%     plot(xspan(ind2),u(ind2),'red','LineWidth',2);
    %scatter(xspan,u,40,Fr,'filled');
    %plot(xspan,u,'black');
    %colorbar

z = Fr>1;
patch([xspan' nan],[u' nan],[z' nan],[z' nan], 'edgecolor', 'interp','linewidth',2); 
map = [0.0745 0.62 1; 1 0 0];
colormap(map);
%c = colorbar;
%c.Label.String = 'Fr';
%c.Position = [0.1 0.1 0.3 0.7];


    %z = zeros(size(xspan'));
    %col = Fr;

%     surface([xspan';xspan'],[u';u'],[z;z],[col;col],...
%         'facecol','no',...
%         'edgecol','interp',...
%         'linew',2);
% 
%     cd = colormap('parula'); % take your pick (doc colormap)
%     cd = interp1(linspace(min(Fr),max(Fr),length(cd)),cd,Fr); % map color to y values
%     cd = uint8(cd'*255); % need a 4xN uint8 array
%     cd(4,:) = 255; % last column is transparency
%     set(res.Edge,'ColorBinding','interpolated','ColorData',cd)

    %plot(xspan, u.*D);
    %plot(xspan,Fr,'LineWidth',2);

    
%     str = ['Fr = ', num2str(Fr)];
%     title(str);
    
    %legend(num2str(uvals)');

    %legend('h','D+h');

    %title('D=1, u=12, Fr=15');
    
    xlabel('Longitude');
    ylabel('Wind speed');

    %legend(num2str(Fr_init'));
    title('3 sample windspeed solutions');

    set(gca,'TickLength',[0.02, 0.05]);
    set(gca,'LineWidth',1);
    box on

    ax = gca;
    ax.FontSize = 15;
end



%% functions

% handles the shock worse
% function dydx = fun(x,y,xspan,dh,g)
% dh_an = interp1(xspan,dh,x);
% dydx = [-g*dh_an ./ (y(1)-y(2)./y(1)); -g*dh_an ./ (-y(1).^2./y(2)+g)];
% end

function dydx_1D = fun2(x,y,xspan,dh,g,u1,D1)
dh_an = interp1(xspan,dh,x);
dydx_1D = -g*dh_an ./ (y-(g*u1*D1)./y.^2);
end
