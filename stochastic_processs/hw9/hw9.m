function hw9()
D()
end
function D()
clear all; close all; clc;
h=0.01; sigma=1; t_MAX=10;
W_vector=normrnd(0,sigma*sqrt(h),1,t_MAX/h);
X_vector=cumsum(W_vector);
plot(h:h:t_MAX,X_vector,'r','Linewidth',1);
xlabel('time');title(['Weiner Process Simulated, h=',num2str(h)]);
grid on; axis([0 t_MAX -5 5])
end
