function hw8
E()
H()
I()
end


function [X,T]=cashflow1(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max)
 index=1;
 X(index)=X_0;
 T(index)=0;
 while T(index)<T_max
     x=X(index);
     if x==0 %only premium is possible
         tau=exprnd(1/lambda);
         T(index+1)=T(index)+tau;
         X(index+1)=x+1;
     elseif 0<x && x<c %premium, claim payed at X(t) not c
         tau=exprnd(1/(lambda+alpha));
         T(index+1)=T(index)+tau;
         u=rand;
                                   if u<(lambda/(lambda+alpha))
    X(index+1)=x+1;
else            % claim
    X(index+1)=0;
% premium
            end
elseif c<=x && x<X_r %premium, claim
    tau=exprnd(1/(lambda+alpha));
    T(index+1)=T(index)+tau;
    u=rand;
    if u<(lambda/(lambda+alpha))   %
        X(index+1)=x+1;
    else
              
          X(index+1)=x-c;
    end
elseif X_r<=x && x<X_max %premium, claim, dividend
    tau=exprnd(1/(lambda+alpha+beta));
    T(index+1)=T(index)+tau;
    u=rand;
    if u<(lambda/(lambda+alpha+beta))  % premium
        X(index+1)=X(index)+1;
    elseif u<((lambda+alpha)/(lambda+alpha+beta))  % claim
        X(index+1)=X(index)-c;
                            else    % dividend
            X(index+1)=X(index)-d;
        end
    elseif x==X_max % claim, dividend
        tau=exprnd(1/(alpha+beta));
        T(index+1)=T(index)+tau;
        u=rand;
        if u<(alpha/(lambda+alpha))
            X(index+1)=x-c;
        else          % dividend
            X(index+1)=x-d;
        end
    else
        disp('Out Of Range')
        break
end
    index=index+1;
end
end

function E()
clc; clear all; close all;
X_0=200;
N=200;
r=0.04;
lambda=N;
alpha=r*N;
beta=4;
X_r=200;
X_max=300;
T_max=5;
d=30;
c=20;
[X,t]=cashflow1(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max);
% Plotting the results
hold on
grid on
xlabel('time','Fontsize',14)
ylabel('Cash Level','Fontsize',14)
title('(a sample) Evolution of Cash Level over 5 Years','Fontsize',14)
axis([0 5 0 310])
stairs(t,X,'Linewidth',2,'Color','r');
end

function H()
R=Kolmogrov_F(lambda,alpha,beta,c,d,X_r,X_max);
 p0=zeros(X_max+1,1);
 p0(X_0+1,1)=1;
 T=0:0.25:5;
 figure
 hold on
 xlabel('X','Fontsize',14)
 ylabel('pmf','Fontsize',14)
 title('pmf of the states between 0 and 5 over quarterly intervals','Fontsize',14)
 axis([0 300 0 0.016])
 for t=T
     pmf=expm(R.*t)*p0;
     plot(0:X_max,pmf,'r')
 end
end
function [R]=Kolmogrov_F(lambda,alpha,beta,c,d,X_r,X_max)
 R=zeros(X_max+1); % initialization
 % Range A:
 R(1,1)=-lambda;
 R(1,2:c+1)=alpha;
 % Range B:
 for i=2:c
     R(i,i-1)=lambda;
     R(i,i+c)=alpha;
     R(i,i)=-(lambda+alpha);
end
 % Range C-1:
 for i=c+1:X_r-d
     R(i,i-1)=lambda;
     R(i,i+c)=alpha;
     R(i,i)=-(lambda+alpha);
end
 % Range C_2:
 for i=X_r-d+1:X_r
     R(i,i-1)=lambda;
     R(i,i+c)=alpha;
     R(i,i+d)=beta;
     R(i,i)=-(lambda+alpha);
end
 % Range D_1:
 for i=X_r+1:X_max-d+1
     R(i,i-1)=lambda;
     R(i,i+c)=alpha;
     R(i,i+d)=beta;
     R(i,i)=-(lambda+alpha+beta);
end
 % Range D_2:
 for i=X_max-d+2:X_max-c+1
     R(i,i-1)=lambda;
     R(i,i+c)=alpha;
     R(i,i)=-(lambda+alpha+beta);
end
 % Range D_3:
 for i=X_max-c+2:X_max
     R(i,i-1)=lambda;
     R(i,i)=-(lambda+alpha+beta);
 end
 % Range E:
 R(X_max+1, X_max)=lambda;
 R(X_max+1, X_max+1)=-(alpha+beta);
end

function I()
R=Kolmogrov_F(lambda,alpha,beta,c,d,X_r,X_max);
p0=zeros(X_max+1,1);
p0(X_0+1,1)=1;
T=0.25:0.25:5;
prob=zeros(20,1);
figure
hold on
xlabel('time (years)','Fontsize',18)
ylabel('Prob. of dividend','Fontsize',18)
axis([0 5 0.2 0.30])
for t=T
        pmf=expm(R.*t)*p0;
        prob(t/0.25) = sum(pmf(201:end))*0.64;
end
set(gca, 'fontsize', 16)
stairs(T,prob,'Linewidth',2,'Color','r');
grid on
end