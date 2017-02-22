function hw1

% A
function [ret,t,b] = simulator(w0,p,T)
    m=w0;
    t=0;
    b=0;
    time=0;
    for i = 0:T-1
        rand1=random('bino',1,p);
        if rand1==1
            w0=w0+1;
        else 
            w0=w0-1;
        end
        time=time+1;
        if b==1
            m=[m,0];
        elseif w0==0 && b==0
            m=[m,0];
            b=1;    
            t=time;
        else  
            m=[m,w0];
        end    
    end 
    ret= m;
    
end



a=simulator(20,0.25,1000);
b=simulator(20,0.5,1000);
c=simulator(20,0.75,1000);
plot(0:1000,a,0:1000,b,0:1000,c);




% B
function p=simulator2(t,w0,p)
    zero=0;
    one=0;
    for k=0:t-1
        [a,b,c]=simulator(w0,p,100);
        if c==0
            zero=zero+1;
        end
        if c==1
            one=one+1;
        end
        
    end 
    
    p=one/(zero+one);
end



x=[];
y=[];
for j=1:100
    p=simulator2(100+j*20,10,0.55);
    x=[x,100+j*20];
    y=[y,p];
end

plot(x,y)


% C 
%% Setting N==2000 for all w0
y=[];
for j=1:20
    p=simulator2(2000,j,0.55);
    y=[y,p];
end
plot(1:20,y)

% D
%% Setting N=2000

y=[];
x=[];
for j=0:20
    p=simulator2(2000,10,0.3+j*0.02);
    y=[y,p];
    x=[x,0.3+j*0.02];
end
plot(x,y)


% E
function t=infiSimi(w0,maxt,p)
    t=maxt;
    for i =1:maxt
        rand1=random('bino',1,p);
        if rand1==0
            w0=w0-1;
        
        else
            w0=w0+1;
        end    
        
        if w0==0
            t=i;
            break
        end
    end    
end    

x=[];
for i= 1:2000
   t=infiSimi(10,200,0.4);
   x=[x,t];
end

disp(mean(x))
histogram(x)

end