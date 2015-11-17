
function [outputPieces, outputBoard] = task1()
    
    outputPieces = {};
    outputBoard = {};
    
    
    % Read inn the image, and spereta the channels to be able to catch all
    % the game pices
    I = imread('image1.png');
    I_red = I(:,:,1);
    I_green = I(:,:,2);
    I_blue = I(:,:,3);
    
    outputBoard = [impixel(I,50,50) , impixel(I,150,50)];
    
    % Red channel only
    BW_red = im2bw(I_red,0.3);
    SOBEL_red = edge(BW_red,'Sobel');

    % Green channel only
    BW_green = im2bw(I_green,0.3);
    SOBEL_green = edge(BW_green,'Sobel');
    
    % Green channel only
    BW_blue = im2bw(I_green,0.015);
    SOBEL_blue = edge(BW_blue,'Sobel');
    
    
    %Combine the channels into one image
    RB = imfuse(SOBEL_blue, SOBEL_red);
    RGB = imfuse(RB, SOBEL_green);
    
    %Turn the combined processed image into one BW image.
    BW = im2bw(RGB,.2);
    
    % Find all the images in the range given.
    [centers, radii, metric] = imfindcircles(BW,[30 45],'Sensitivity',0.90,'EdgeThreshold',0.15);
       
    for idx = 1:numel(radii)
         line = [ centers(idx),centers(idx+numel(radii)),radii(idx),impixel(I,centers(idx),centers(idx+numel(radii)))];
         outputPieces(end+1) = {line}
    end
    
    imshow(BW);
    hBright = viscircles(centers, radii,'EdgeColor','b');
    
end

