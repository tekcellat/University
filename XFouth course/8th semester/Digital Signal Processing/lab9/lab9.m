I = double(imread('bimage3.bmp')) / 255; %bw image

figure(1);
imshow(I);
title('Original image');

PSF = fspecial('motion', 55, 65); % if u use it for other img, u need play
% with this 2 numbers, it's ur PSF. Theta is angle of blur (0-360)
% Anyway, u'll get some artefacts on borders, it's okay :)
% Also it can be not motion blur, disk, then
% PSF = fspecial('disk', 10); this number is radius.

[J1, P1] = deconvblind(I, PSF);
figure(2);
imshow(J1);
title('Recovered image');
