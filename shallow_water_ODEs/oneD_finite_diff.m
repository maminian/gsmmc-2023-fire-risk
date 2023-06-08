clear;
clc;
close all

N = 1000;

xspan = linspace(-1,2,N);
%h = exp(-((xspan-1)/.1).^2)/2;
h = -exp(-((xspan-1/2)/.1).^2)/2 + exp(-(xspan/.1).^2)/2;
dh = gradient(h)./gradient(xspan);
g = 9.8;


%% ode45 (Runge-Kutta)


u1 = 5;
Dvals = 5; % subcritical
%uvals = 12;

figure;
hold on
plot(xspan,h,'LineWidth',2);

for j=1:size(Dvals,2)
    D1 = Dvals(j);


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
    plot(xspan,Fr,'LineWidth',2);

    
%     str = ['Fr = ', num2str(Fr)];
%     title(str);
    
    %legend(num2str(uvals)');

    %legend('h','D+h');

    %title('D=1, u=12, Fr=15');
    
    xlabel('x');

    legend('topography','flow speed','Froude number');

    set(gca,'TickLength',[0.02, 0.05]);
    set(gca,'LineWidth',1);
    box on

    ax = gca;
    ax.FontSize = 15;
end





% %% forward Euler -- DO NOT USE
% u = zeros(N,1);
% D = zeros(N,1);
% ds = (xspan(end) - xspan(1)) / N;
% % u(1) = 1;
% % D(1) = 1;
% 
% u(1) = 6;
% Dvals = [1/2, 1, 3, 6, 8];
% 
% figure;
% 
% for j=1:size(Dvals,2)
%     D(1) = Dvals(j);
% 
%     Fr = u(1)^2/(g*D(1)^2);
% 
%     for i=1:N-1
%         D(i+1) = D(i) + ds * (1 - g*D(i)/u(i)^2)^(-1) * g * D(i)/u(i)^2 * dh(i);
%     %     if D(i+1) < h(i+1) % make sure the fluid height doesn't drop below the mountain
%     %         D(i+1) = h(i+1);
%     %     end
%         u(i+1) = u(i) * (1 - (D(i+1)-D(i))/D(i));
%     end
%     
%     
%     subplot(3,2,j);
%     plot(xspan,D+h');
%     hold on
%     plot(xspan,h);
%     
%     str = ['Fr = ', num2str(Fr)];
%     title(str);
%     
%     legend('D','h');
%     
%     xlabel('x');
%     ylabel('y');
% 
%     set(gca,'TickLength',[0.02, 0.05]);
%     set(gca,'LineWidth',1);
% 
%     ax = gca;
%     ax.FontSize = 15;
% end


%% functions

function dydx = fun(x,y,xspan,dh,g)
dh_an = interp1(xspan,dh,x);
dydx = [-g*dh_an ./ (y(1)-y(2)./y(1)); -g*dh_an ./ (-y(1).^2./y(2)+g)];
end

function dydx_1D = fun2(x,y,xspan,dh,g,u1,D1)
dh_an = interp1(xspan,dh,x);
dydx_1D = -g*dh_an ./ (y-(g*u1*D1)./y.^2);
end















