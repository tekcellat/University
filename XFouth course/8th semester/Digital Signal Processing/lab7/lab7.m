A = 1.0;
s1 = 1.0;
s2 = 2.0;

% bord
mult = 10;
step = 0.005;
t = -mult:step:mult;

% sig gen
u1 = gauspls(t, A, s1);
v1 = fft(u1);

u2 = gauspls(t, A, s2);
v2 = fft(u2);

% silent
NS = 0.05;

n1 = unifrnd(-NS, NS, 1, length(t));
n2 = unifrnd(-NS, NS, 1, length(t));

delta = std(n1);
epsilon = std(n2);

figure(1);
plot(t, u1 + n1, 'k', t, u2 + n2, 'r', t, abs(ifft(fft(u2 + n2) .* tikhonfilt(v1, v2, step, 2 * mult, delta, epsilon))), 'g');
title('lab7');
legend('Original sig u1', 'Distorted signal u2', 'Get signal');

% gen gauss sig
function y = gauspls(x, A, s)
    y = A * exp(-(x / s).^2);
end

%Tixanov filter
function h = tikhonfilt(u1, u2, step, T, d, e)
    m = 0:length(u1) - 1;
    mult = step / length(u1);

    squ = 1 + (2 * pi * m / T).^2;

    func = @(x) rhofunc(x, u1, u2, step, T, d, e);
    alpha = 0.001;

    h = 0:length(u1) - 1;

    for k = 1:length(h)
        h(k) = mult * sum(exp(2 * pi * 1i * k .* m / length(u1)) .* u1 .* conj(u2) ./ (abs(u2).^2 .* step^2 + alpha * squ), 2);
    end

end

% Rho-function
function y = rhofunc(x, u1, u2, step, T, d, e)
    m = 0:length(u1) - 1;
    mult = step / length(u1);

    squ = 1 + (2 * pi * m / T).^2;

    beta = mult * sum(x.^2 * squ .* abs(u1).^2 ./ (abs(u2).^2 * step^2 + x .* squ).^2, 2);
    gamma = mult * sum(abs(u2).^2 * step^2 .* abs(u1).^2 .* squ ./ (abs(u2).^2 * step^2 + x * (1 + 2 * pi * m / T).^2).^2, 2);

    y = beta - (d + e * sqrt(gamma))^2;
end
