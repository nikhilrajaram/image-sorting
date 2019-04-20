function img = scale_image(img, height, width, grayscale)
    img = imresize(img, [height, width]);
    if ((grayscale) && (length(size(img)) == 3))
        img = rgb2gray(img);
    end
end
