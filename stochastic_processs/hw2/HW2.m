function HW2
% A
series=[6,10,20,50];

figure(1)
j=0;
for i = series
    n=i;
    p=5.0/n;
    subplot(2,2,1+j);
    stem(0:n,pdf('bino',0:n,n,p),'.');  
    j=j+1;
end
saveas(figure(1),'./fig1.png')

figure(2)
j=0;
for i = series
    n=i;
    p=5.0/n;
    subplot(2,2,1+j);
    plotbrowser('off')
    stem(0:n,cdf('bino',0:n,n,p),'.');
    j=j+1;
end
saveas(figure(2),'./fig2.png')

% B
figure(3)
stem(0:50,pdf('poiss',0:50,5),'.')
saveas(figure(3),'./fig3.png')



x=2:8;
i=0;

my_MSE=zeros(1,4);
for n=series
    i=i+1;
    my_poisson_pmf=exp(-5)*(5.^x)./factorial(x);
    my_MSE(1,i)=sum((pdf('bino',x,n,5/n)-my_poisson_pmf).^2.*my_poisson_pmf);
end

figure(4)
stem(series,my_MSE,'.');
xlabel('n'); ylabel('MSE');
grid on; axis([0,50,0,0.02]);
saveas(figure(4),'./fig4.png')

my_MSE
close all;

% D
j=0;


figure(5)
for k =[10,20,50]
    x=0:k;
    j=j+1;
    subplot(3,1,j)
    stairs(0:k,[(cdf('bino',0:k,k,0.5))', ...
        cdf('normal',x,k*0.5,sqrt(k*0.5*0.5))'],'LineWidth',2);
    legend('Binomial','Normal');
     grid on; axis([0,50,0,1]);

end

saveas(figure(5),'./fig5.png')

close all;
end

