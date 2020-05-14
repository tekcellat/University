function lab1()
    clear all;
    X = [0.70,-0.35,-0.23,-1.18,-0.75,0.41,-0.71,0.97,-2.54,-1.50,1.73,-0.83,-1.13,-0.00,-0.40,1.23,-0.14,-1.38,0.01,-1.65,0.02,-1.61,0.46,1.19,-1.30,0.32,1.19,-0.03,-0.31,-1.64,-0.24,0.30,-0.66,-1.31,-0.65,0.63,-0.27,1.04,0.20,0.31,0.24,1.27,-0.17,-0.62,0.03,-1.75,-2.26,-0.03,-0.27,-0.17,0.10,-0.14,0.09,0.53,-0.78,-0.86,0.35,-0.72,-0.41,0.38,-0.91,-0.41,-1.10,-1.00,0.39,-0.06,0.32,-1.58,-0.14,-0.90,-1.84,0.00,-0.10,-1.14,-0.14,0.82,-2.55,-2.79,-0.02,-0.66,-0.05,-0.15,-1.68,1.62,0.21,-0.01,-0.33,0.68,1.80,-0.29,-0.74,-0.38,-2.67,-1.53,-0.48,0.66,-0.56,0.28,0.70,1.01,0.53,0.93,-1.27,-1.37,-0.29,-2.18,-1.02,0.21,0.19,1.75,-0.01,0.30,-0.73,0.34,-0.23,1.13,-1.13,-0.96,0.37,0.14];
    X = sort(X);
    
    Mmax = max(X);
    Mmin = min(X);
    
    fprintf('Mmin = %s\n', num2str(Mmin));
    fprintf('Mmax = %s\n', num2str(Mmax));
    
    R = Mmax - Mmin;
    fprintf('R = %s\n', num2str(R));
    
    MU = getMU(X);
    fprintf('MU = %s\n', num2str(MU));
    
    Ssqr = getSsqr(X);
    fprintf('S^2 = %s\n', num2str(Ssqr));
    
    m = getNumberOfIntervals(X);
    fprintf('m = %s\n', num2str(m))
    
    createGroup(X);
    hold on;
    distributionDensity(X, MU, Ssqr, m);

    figure;
    empiricF(X);
    hold on;
    distribution(X, MU, Ssqr, m);
end

function mu = getMU(X)
    n = length(X);
    mu = sum(X)/n;
end

function Ssqr = getSsqr(X)
    n = length(X);
    MX = getMU(X);
    Ssqr = sum((X - MX).^2) / (n-1);
end

function m = getNumberOfIntervals(X)
    m = floor(log2(length(X)) + 2);
end

function createGroup(X)
    n = length(X);
    m = getNumberOfIntervals(X);
    
    intervals = zeros(1, m+1);
    numCount = zeros(1, m+1);
    Delta = (max(X) - min(X)) / m;
    
    for i = 0: m
        intervals(i+1) = X(1) + Delta * i;
    end
    
    j = 1;
    count = 0;
    for i = 1:n
        if (X(i) >= intervals(j+1)) 
            j = j + 1; 
        end
        numCount(j) = numCount(j) + 1;
        count = count + 1;
    end

	graphBuf = numCount(1:m+1);
    for i = 1:m+1
        graphBuf(i) = numCount(i) / (n*Delta); 
    end
    
    stairs(intervals, graphBuf),grid;
end

function distributionDensity(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    Sigma = sqrt(DX);
    
    Xn = (MX - R): delta/50 :(MX + R);
    Y = normpdf(Xn, MX, Sigma);
    plot(Xn, Y), grid;
end

function distribution(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    
    Xn = (MX - R): delta :(MX + R);
    Y = 1/2 * (1 + erf((Xn - MX) / sqrt(2*DX))); 
    plot(Xn, Y, 'r'), grid;
end

function empiricF(X)  
    [yy, xx] = ecdf(X);
    
    stairs(xx, yy), grid;
end