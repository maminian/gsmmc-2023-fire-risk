clear;
clc;
close all

N = 1000;

u = zeros(N,1);
D = zeros(N,1);
xspan = linspace(-1,1,N);

h = exp(-(xspan/.3).^2)/2;

dh = gradient(h)./gradient(xspan);

g = 9.8;

ds = (xspan(end) - xspan(1)) / N;






%%


% forward Euler

% u(1) = 1;
% D(1) = 1;

% u(1) = 5;
% D(1) = 1/2;

u(1) = 4;
D(1) = 8;

Fr = u(1)^2/(g*D(1)^2);

for i=1:N-1
    D(i+1) = D(i) + ds * (1 - g*D(i)/u(i)^2)^(-1) * g * D(i)/u(i)^2 * dh(i);
    if D(i+1) < h(i+1) % make sure the fluid height doesn't drop below the mountain
        D(i+1) = h(i+1);
    end
    u(i+1) = u(i) * (1 - (D(i+1)-D(i))/D(i));
end


figure;
plot(xspan,D+h');
hold on
plot(xspan,h);

str = ['Fr = ', num2str(Fr)];
title(str);

legend('D','h');

xlabel('x');
ylabel('y');


% 
% %% RK4, ode45 (DOESN'T WORK YET)
% 
% [xspan,y] = ode45(@(x,y)fun(x,y,dh),xspan,[u(1); D(1)]);
% 
% function dydx = fun(x,y,dh)
% dh_an = interp1(x,dh,x);
% dydx = [-g*dh_an ./ (y(1)-y(2)./y(1)); -g*dh_an ./ (-y(1).^2./y(2)+g)];
% end



