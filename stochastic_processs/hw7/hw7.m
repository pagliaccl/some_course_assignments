function hw7()
    A()
    C()
end
function A()
clc; clear all; close all
 T=10;      
 lambda= 1; 
 nr_experiments=10^4;
 n=1000;
 h=T/n;
 p = lambda*h;
 
 arrival = binornd(1,p,n,nr_experiments);
 x=0:30;
 pdf_approx = hist(sum(arrival),x)/nr_experiments;
 bar(x,pdf_approx,'r')
 hold on
 plot(x,poisspdf(x,lambda*T),'b','Linewidth', 2)
 xlabel('t','Fontsize',12)
 ylabel('pmf','Fontsize',12)
 title('pmf of number of arrivals for a Poisson Process of \lambda=1, and for T=10',...
    'Fontsize',12)
 legend('Estimated','Calculated','Location','Best')
 figure
 pdf_approx = hist(sum(arrival(1:n/2,:)),x)/nr_experiments;
 bar(x,pdf_approx,'r')
 hold on
 plot(x,poisspdf(x,lambda*T/2),'b','Linewidth', 2)
 xlabel('t','Fontsize',12)
 ylabel('pmf','Fontsize',12)
 title('pmf of number of arrivals for a Poisson Process of \lambda=1,and for T=5',...
     'Fontsize',12)
 legend('Estimated','Calculated','Location','Best')
end

function C()
clc; clear all; close all
 T=10;      
 lambda= 1; 
 nr_experiments=10^4;
 n=1000;
 h=T/n;
 p = lambda*h;
 
 arrival = binornd(1,p,n,nr_experiments);
 
 first_arrival_times=n*ones(1,nr_experiments);
 nr_arrived=cumsum(arrival);
 for i=1:nr_experiments
     temp=find(nr_arrived(:,i),1);
     if isempty(temp)
         first_arrival_times(1,i)=temp;
     end
 end
 hist_firs_arrival_times=hist(first_arrival_times,1:n);
 
 time=0;
 experiment=1;
 time_histogram = zeros(n,1);
 while (experiment <= nr_experiments) && (time < n)
     time = time+1;
     if arrival(time, experiment)
         time_histogram(time)=time_histogram(time)+1;
         experiment = experiment+1;
         time=0;
     end
 end
 
 figure
 plot((1:n)*h,hist_firs_arrival_times/nr_experiments/h,'r')
 hold on
 
 plot((1:n)*h,exppdf((1:n)*h,lambda),'b','Linewidth', 2)
 xlabel('t','Fontsize',12)
 ylabel('pdf','Fontsize',12)
 title('pdf of first arrival time for a Poisson Process of \lambda=1,Method 1','Fontsize',12)
 legend('Estimated','Calculated','Location','Best')
 figure
 plot((1:n)*h,time_histogram/nr_experiments/h,'r')
 hold on
 plot((1:n)*h,exppdf((1:n)*h,lambda),'b','Linewidth', 2)
 xlabel('t','Fontsize',12)
 ylabel('pdf','Fontsize',12)
 title('pdf of first arrival time for a Poisson Process of \lambda=1, Method 2','Fontsize',12)
 legend('Estimated','Calculated','Location','Best')
 
 figure
 plot((1:n)*h,cumsum(time_histogram/nr_experiments),'r')
 hold on
 plot((1:n)*h,expcdf((1:n)*h,lambda),'b','Linewidth', 1)
 xlabel('t','Fontsize',12)
 ylabel('cdf','Fontsize',12)
 title('cdf of first arrival time for a Poisson Process of \lambda=1','Fontsize',12)
 legend('Estimated','Calculated','Location','Best')


end

