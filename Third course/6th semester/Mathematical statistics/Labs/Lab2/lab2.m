function lab2()
    X=[0.70,-0.35,-0.23,-1.18,-0.75,0.41,-0.71,0.97,-2.54,-1.50,1.73,-0.83,-1.13,-0.00,-0.40,1.23,-0.14,-1.38,0.01,-1.65,0.02,-1.61,0.46,1.19,-1.30,0.32,1.19,-0.03,-0.31,-1.64,-0.24,0.30,-0.66,-1.31,-0.65,0.63,-0.27,1.04,0.20,0.31,0.24,1.27,-0.17,-0.62,0.03,-1.75,-2.26,-0.03,-0.27,-0.17,0.10,-0.14,0.09,0.53,-0.78,-0.86,0.35,-0.72,-0.41,0.38,-0.91,-0.41,-1.10,-1.00,0.39,-0.06,0.32,-1.58,-0.14,-0.90,-1.84,0.00,-0.10,-1.14,-0.14,0.82,-2.55,-2.79,-0.02,-0.66,-0.05,-0.15,-1.68,1.62,0.21,-0.01,-0.33,0.68,1.80,-0.29,-0.74,-0.38,-2.67,-1.53,-0.48,0.66,-0.56,0.28,0.70,1.01,0.53,0.93,-1.27,-1.37,-0.29,-2.18,-1.02,0.21,0.19,1.75,-0.01,0.30,-0.73,0.34,-0.23,1.13,-1.13,-0.96,0.37,0.14];

    N = 1:length(X);
    
    gamma = 0.9;
    alpha = (1 - gamma)/2;

    mu = expectation(X);
    sSqr = variance(X); 

    fprintf('mu = %.4f\n', mu); 
    fprintf('S^2 = %.4f\n\n', sSqr);

    muArray = expectationArray(X, N);
    varArray = varianceArray(X, N);
 
    figure
    plot([N(1), N(end)], [mu, mu], 'm');
    hold on;
    plot(N, muArray, 'g');
    
    Ml = muArray - sqrt(varArray./N).*tinv(1 - alpha, N - 1);
    plot(N, Ml, 'b');

    fprintf('mu_low = %.4f\n', Ml(end));
    
    Mh = muArray + sqrt(varArray./N).*tinv(1 - alpha, N - 1);
    plot(N, Mh, 'r'), legend('y=mu', 'y=mu_n', 'y=mu-low_n', 'y=mu-high_n');
    grid on;
    hold off;
    
    fprintf('mu_high = %.4f\n', Mh(end));

    figure
    plot([N(1), N(end)], [sSqr, sSqr], 'm');
    hold on;
    plot(N, varArray, 'g');
    
    Sl = varArray.*(N - 1)./chi2inv(1 - alpha, N - 1);
    plot(N, Sl, 'b');
    
    Sh = varArray.*(N - 1)./chi2inv(alpha, N - 1);
    plot(N, Sh, 'r'), legend('z=S^2', 'z=S^2_n', 'z=S^2-low_n', 'z=S^2-high_n');
    grid on;
    hold off;

	
    fprintf('sigma^2_low = %.4f\n', Sl(end));
    fprintf('sigma^2_high = %.4f\n', Sh(end));
end

function mu = expectation(X)
   mu = mean(X);
end

function sSqr = variance(X)
    sSqr = var(X);
end

function muArray = expectationArray(X, N)
    muArray = zeros(1, length(N));
    for i = 1:length(N)
        muArray(i) = expectation(X(1:N(i)));
    end
end

function varArray = varianceArray(X, N)
    varArray = zeros(1, length(N));
    for i = 1:length(N)
        varArray(i) = variance(X(1:N(i)));
    end
end
