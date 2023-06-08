%% Three bodies problem

%%  Obtained from:
% andrea (2022). Three body problem
% (https://www.mathworks.com/matlabcentral/fileexchange/96932-three-body-problem),
% MATLAB Central File Exchange. Retrieved May 1, 2022.



clc
clear all
close all

% Time step [s]
step = 0.001 ;

% Body Mass
m1 = 1;
m2 = 1;
m3 = 1;

M = [m1 ; m2 ; m3] ;

% Newton constant
G = 1;

% Time vector
t = 0:step:5 ;

% Initial conditions -- positions
% Initial condiition were taken from:

%{
Numerical Search for Periodic Solutions in the Vicinity of the
Figure-Eight Orbit: Slaloming around Singularities on the Shape
Sphere
Milovan ˇSuvakov

%C. Moore, Phys. Rev. Lett. 70, 3675 (1993).
%C. Sim ́o, Contemp Math 292 20928 (2002)

%}

x10 = 0; %-1;
y10 = 1; % 0


x20 = -x10;
y20 = -y10 ;


x30 = 0 ;
y30 = 0 ;



% Initial condition -- velocity

vx10 =  0.3471;
vy10 =  0.5327;

vx20 = vx10;
vy20 = vy10;

vx30 = -2*vx10;
vy30 = -2*vy10;







% Preparing the vector to store the solution
% There are 3 columns since I want to simulate three bodies

x = zeros(numel(t),3) ;
y = zeros(numel(t),3) ;

vx = zeros(numel(t),3);
vy = zeros(numel(t),3);

ax = zeros(3,3);
ay = zeros(3,3);


% Assign the initial condition to the first element of  the solution vectors

x(1,1) = x10 ;
x(1,2) = x20 ;
x(1,3) = x30 ;

y(1,1) = y10 ;
y(1,2) = y20 ;
y(1,3) = y30 ;

vx(1,1) = vx10  ;
vx(1,2) = vx20  ;
vx(1,3) = vx30  ;

vy(1,1) = vy10 ;
vy(1,2) = vy20 ;
vy(1,3) = vy30 ;





%% Simple euler method

% loop over each time step
for i = 1:length(t)

        % Compute the current accelleration
         [ax_tot,ay_tot] = compute_a (x(i,:),y(i,:),M,ax,ay,G) ;

        % Update the position
         x(i+1,:) = x(i,:) + step*vx(i,:) ;
         y(i+1,:) = y(i,:) + step*vy(i,:) ;

        % Update the velocity
         vx(i+1,:)  = vx(i,:) + step * ax_tot;
         vy(i+1,:)  = vy(i,:) + step * ay_tot;

end

figure(1)
hold on
grid on

title ( 'Simple Euler method' )
xlabel('x')
ylabel('y')

plot (x(:,1),y(:,1),'r')
plot (x(:,2),y(:,2),'g')
plot (x(:,3),y(:,3),'b')
plot ( x10, y10, 'ro', 'MarkerFaceColor','r')  ;
plot ( x20, y20, 'go', 'MarkerFaceColor','g')  ;
plot ( x30, y30, 'bo', 'MarkerFaceColor','b')  ;
legend ('Body 1','Body 2','Body 3')


%% Verlet method

% Preparing again the vector to store the solution
% There are 3 columns since I want to simulate three bodies

x = zeros(numel(t),3) ;
y = zeros(numel(t),3) ;

vx = zeros(numel(t),3);
vy = zeros(numel(t),3);

ax = zeros(3,3);
ay = zeros(3,3);


% Assign the initial condition to the first element of  the solution vectors

x(1,1) = x10 ;
x(1,2) = x20 ;
x(1,3) = x30 ;

y(1,1) = y10 ;
y(1,2) = y20 ;
y(1,3) = y30 ;

vx(1,1) = vx10  ;
vx(1,2) = vx20  ;
vx(1,3) = vx30  ;

vy(1,1) = vy10 ;
vy(1,2) = vy20 ;
vy(1,3) = vy30 ;


for i = 1:length(t)

    % Compute the acceleration at the current time
     [ax_tot,ay_tot] = compute_a (x(i,:),y(i,:),M,ax,ay,G) ;

    % Compute the next time position given the the current accelleration
    x(i+1,:) = x(i,:) + step*vx(i,:) + 1/2 * (ax_tot * step^2) ;
    y(i+1,:) = y(i,:) + step*vy(i,:) + 1/2 * (ay_tot * step^2) ;

    % Compute the next time accelleration
    [ax_tot_next,ay_tot_next] = compute_a (x(i+1,:),y(i+1,:),M,ax,ay,G) ;

    % Compute the next time velocity according to the Verlet method
    vx(i+1,:) = vx(i,:) + 1/2 * ( ax_tot + ax_tot_next ) * step ;
    vy(i+1,:) = vy(i,:) + 1/2 * ( ay_tot + ay_tot_next ) * step ;


end


figure(2)

title ( 'verlet method' )
xlabel('x')
ylabel('y')

hold on
grid on

plot (x(:,1),y(:,1),'r')
plot (x(:,2),y(:,2),'g')
plot (x(:,3),y(:,3),'b')
plot ( x10, y10, 'ro', 'MarkerFaceColor','r')  ;
plot ( x20, y20, 'go', 'MarkerFaceColor','g')  ;
plot ( x30, y30, 'bo', 'MarkerFaceColor','b')  ;
legend ('Body 1','Body 2','Body 3')



%% Compute accelleration

function [ax_tot,ay_tot] = compute_a(x,y,M,ax,ay,G)

% Loop over the three bodies
 for j=1:3

        % Compute the distance between current body and the others ( also
        % with itself )
        dx = ( x(j)-x )' ;
        dy = ( y(j)-y )' ;

        % Compute the acceleration according to Newton law
        ax(:,j) =  (-dx.*M*G)./(sqrt (dx.^2 + dy.^2 )).^3  ;
        ay(:,j) =  (-dy.*M*G)./(sqrt (dx.^2 + dy.^2 )).^3 ;


    % change NaN into zeros
	% the NaN comes when computing the interaction of a body with itself since (dx,dy,dz) = 0

        ax ( isnan(ax)) = 0 ;
        ay ( isnan(ay)) = 0 ;

        ax_tot = sum(ax,1) ;
        ay_tot = sum(ay,1) ;

 end

end


