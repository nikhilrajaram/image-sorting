% very similar
I1 = imread('../img/IMG_20180713_143820_2.jpg');
I2 = imread('../img/IMG_20180713_143819_2.jpg');

% somewhat similar
I3 = imread('../img/IMG_20180713_150338.jpg');
I4 = imread('../img/IMG_20180713_150328.jpg');

% dissimilar
I5 = imread('../img/20160708_140405.jpg');
I6 = imread('../img/paris_general_000076.jpg');

height = 300;
width = 300;

[features_1, valid_points_1] = extract_SURF_features(I1, height, width);
[features_2, valid_points_2] = extract_SURF_features(I2, height, width);
[features_3, valid_points_3] = extract_SURF_features(I3, height, width);
[features_4, valid_points_4] = extract_SURF_features(I4, height, width);
[features_5, valid_points_5] = extract_SURF_features(I5, height, width);
[features_6, valid_points_6] = extract_SURF_features(I6, height, width);

disp(length(matchFeatures(features_1, features_2))/min(length(features_1), length(features_2)));
disp(length(matchFeatures(features_2, features_3))/min(length(features_2), length(features_3)));
disp(length(matchFeatures(features_3, features_4))/min(length(features_3), length(features_4)));
disp(length(matchFeatures(features_4, features_5))/min(length(features_4), length(features_5)));
disp(length(matchFeatures(features_5, features_6))/min(length(features_5), length(features_6)));
