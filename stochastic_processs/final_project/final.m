function final()
    F('/Users/Pagliacci/Desktop/F.png')
    I('/Users/Pagliacci/Desktop/I.png')
    K('/Users/Pagliacci/Desktop/K.png')
    
end 

function F(dir)
    mu=1/(56/60); 
    lambda=25; 
    TMin=1800;
    TMax=30; 
    K=32; 
    X0=0;
    [X,T]=HelperF(X0,mu,lambda,K,TMax,dir); 
    f=stairs(T,X')
    saveas(f,dir,'png')
end


function [X,T]=HelperF(X0,mu,lambda,K,TMax,dir) 
close all; clc
counter=1;
X(counter)=X0;
T(counter)=0;
    while T(counter)<TMax 
        x=X(counter);
        if x>=0 && x<K 
            taw=exprnd(1/(lambda+mu*x)); 
            T(counter+1)=T(counter)+taw; 
            u=rand;
            if u<((x*mu)/(lambda+x*mu))
                X(counter+1)=x-1; 
            else
                X(counter+1)=x+1; 
            end
            elseif x==K 
                taw=exprnd(1/(x*mu));
                 %appdending result
                X(counter+1)=x-1;
                T(counter+1)=T(counter)+taw;
                
             
        else
            break
        end
        counter=counter+1; 
    end
end


function I(dir)
    clc; close all;
    X0=0;
    mu=1/(56/60);
    lambda=25;
    K=32;
    figure(1)
    l=[10, 100, 500,1000]
    for i=1:4;
        subplot(2,2,i)
        HelperI(X0,mu,lambda,K,l(i));
        title(['tMax=',num2str(l(i))])
        grid on
    end
    saveas(figure(1),dir,'png')
end



function [Prob]=HelperI(X0,mu,lambda,K,TMax)
    timePast=zeros(1,K+1);
    x=X0;
    t=0;
    while t<TMax
        if x>=0 && x<K
        taw=exprnd(1/(lambda+mu*x));
        t=t+taw;
        timePast(x+1)=timePast(x+1)+taw; 
        
        u=rand;
        if u<((x*mu)/(lambda+x*mu))
            x=x-1;
        else
            x=x+1; 
        end
        elseif x==K 
            taw=exprnd(1/(x*mu));
            t=t+taw;
            timePast(x+1)=timePast(x+1)+taw; 
            x=x-1;
        else
            break 
        end
    end
    Prob=timePast/t; 
    bar(0:K,Prob,'b');
end


function K(dir)
    mu=1/(56/60);
    lambda=(700:10:1100);
    K=32;
    figure(2)
    pb=zeros(1,3);
    i=0;
    for L=lambda/30;
        i=i+1;
        pb(i)=((L/mu).^K/factorial(K))/(sum((L/mu).^(0:K)./factorial(0:K)));
    end
    plot(lambda,pb,'b')
    hold on
    plot(lambda,0.02*ones(size(lambda)),'black')
    saveas(figure(2),dir,'png')
end 