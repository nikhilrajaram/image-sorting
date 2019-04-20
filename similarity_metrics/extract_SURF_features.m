function [features, valid_points] = extract_SURF_features(I, height, width)
    I = scale_image(I, height, width, true);
    points = detectSURFFeatures(I);
    [features, valid_points] = extractFeatures(I, points);
end