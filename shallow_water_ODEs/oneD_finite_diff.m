clear;
clc;
close all

elev_data = load('elev.mat');
lat_data = load('lat.mat');
lon_data = load('lon.mat');
elev = cell2mat(struct2cell(elev_data));
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
desired_lat = 40.2;
[~,ind] = min( abs( lat(:,1)-desired_lat ) );


slice = elev(ind,:);
new_h = smoothdata(slice,'gaussian');


figure;
hold on
plot(lon(1,:),slice,'LineWidth',2);
plot(lon(1,:),new_h,'LineWidth',2);
title(['Slice at latitude = ', num2str(lat(ind,1))]);
xlabel('Longitude');
ylabel('Elevation');
set(gca,'TickLength',[0.02, 0.05]);
set(gca,'LineWidth',1);
box on

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


%u1 = 270;
D1 = 10000; % subcritical
%uvals = 12;

uvals = [240 270 300];
Fr_init = uvals.^2/(g*D1);

% plot Froude number on separate vertical axis

figure;
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


    hold on
    
    %subplot(3,2,j);
    %plot(xspan,D+h','LineWidth',2);
    plot(xspan,u,'LineWidth',2);
    %plot(xspan, u.*D);
    %plot(xspan,Fr,'LineWidth',2);

    
%     str = ['Fr = ', num2str(Fr)];
%     title(str);
    
    %legend(num2str(uvals)');

    %legend('h','D+h');

    %title('D=1, u=12, Fr=15');
    
    xlabel('Longitude');
    ylabel('Wind speed');

    legend(num2str(Fr_init'));
    title(['Slice at latitude = ', num2str(lat(ind,1))]);

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
