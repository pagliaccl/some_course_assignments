function hw4
 close all; clear;clc;
 x0 = 100;
 max_t = 50;
 max_types = 1000; 
                   
 mu = 1.05;
 q = 10^-2;
 X=zeros(max_types, max_t);
 number_of_types=zeros(1, max_t); 
 X(1:x0,1) = 1;
 number_of_types(1)=x0; 
 number_of_extinct_types=zeros(1,max_t);
                                 
 for n=2:max_t
     number_of_types(n)=number_of_types(n-1);
     for type = 1:number_of_types(n-1);
         for i = 1:X(type,n-1)
             daughters = poissrnd(mu,1,1); 
             mutation = binornd(1,q,1,1); 
             if mutation
                 number_of_types(n) = number_of_types(n)+1;
                 X(number_of_types(n),n) = daughters;
             else
                 X(type,n) = X(type,n) + daughters;
             end 
         end 
         if X(type,n)== 0
           number_of_extinct_types(n)=number_of_extinct_types(n)+1;
         end 
     end 
 end 
 figure(1)    
 subplot(2,2,1)
 plot(1:max_t, X)
 xlabel('generation','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('$q=10?{-2},$ $X_{0}=100,$ $n=50$','FontSize',14,'Interpreter','latex')
 
 subplot(2,2,2)
 stairs(1:max_t, X')
 xlabel('generation','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('$q=10?{-2},$ $X_{0}=100,$ $n=50$','FontSize',14,'Interpreter','latex')
 
 subplot(2,2,3)
 stairs(1:max_t, [number_of_types;number_of_extinct_types]','LineWidth',2)
 xlabel('generation','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('$q=10?{-2},$ $X_{0}=100,$ $n=50$','FontSize',14,'Interpreter','latex')
 axis([0 50 0 number_of_types(end)])
 legend('number of types','number of extinct types','Location','Best')
 
 subplot(2,2,4)
 bar(1:number_of_types(end), X(1:number_of_types(end),max_t),'r')
 xlabel('types','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('Histogram of the final number of women of each type','FontSize',14)
 saveas(figure(1),'./figure1.png')
 
 
 close all; clear;clc;
 x0 = 400;
 max_t = 50;
 max_types = 1000; 
                   
 mu = 1.05;
 q = 0;
 X=zeros(max_types, max_t);
 number_of_types=zeros(1, max_t); 
 X(1:x0,1) = 1;
 number_of_types(1)=x0; 
 number_of_extinct_types=zeros(1,max_t);
                                 
 for n=2:max_t
     number_of_types(n)=number_of_types(n-1);
     for type = 1:number_of_types(n-1);
         for i = 1:X(type,n-1)
             daughters = poissrnd(mu,1,1); 
             mutation = binornd(1,q,1,1); 
             if mutation
                 number_of_types(n) = number_of_types(n)+1;
                 X(number_of_types(n),n) = daughters;
             else
                 X(type,n) = X(type,n) + daughters;
             end 
         end 
         if X(type,n)== 0
           number_of_extinct_types(n)=number_of_extinct_types(n)+1;
         end 
     end 
 end 
 figure(2)    
 subplot(2,2,1)
 plot(1:max_t, X)
 xlabel('generation','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('$q=10?{-2},$ $X_{0}=100,$ $n=50$','FontSize',14,'Interpreter','latex')
 
 subplot(2,2,2)
 stairs(1:max_t, X')
 xlabel('generation','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('$q=10?{-2},$ $X_{0}=100,$ $n=50$','FontSize',14,'Interpreter','latex')
 
 subplot(2,2,3)
 stairs(1:max_t, [number_of_types;number_of_extinct_types]','LineWidth',2)
 xlabel('generation','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('$q=10?{-2},$ $X_{0}=100,$ $n=50$','FontSize',14,'Interpreter','latex')
 axis([0 50 0 number_of_types(end)])
 legend('number of types','number of extinct types','Location','Best')
 
 subplot(2,2,4)
 bar(1:number_of_types(end), X(1:number_of_types(end),max_t),'r')
 xlabel('types','FontSize',14)
 ylabel('number of women of each type','FontSize',14)
 title('Histogram of the final number of women of each type','FontSize',14)
 saveas(figure(2),'./figure2.png')
 
 
end 
