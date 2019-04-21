files = dir('../img/*jpg');
imgs = cell(1, length(files));
features = cell(length(files));

for i=1:length(files)
	imgs{i} = scale_image(imread(strcat('../img/', files(i).name)), 300, 300, true);
	[features{i}, ~] = extract_SURF_features(imgs{i}, 300, 300);
end

compare_idxs = combnk(1:length(files), 2);
is = compare_idxs(:, 1);
js = compare_idxs(:, 2);
sims = zeros(1, length(is));

for i=1:length(is)
	sims(i) = length(matchFeatures(features{is(i)}, features{js(i)}))/max(length(features{is(i)}), length(features{js(i)}));
end
[sims, sims_idx] = sort(sims,'descend');

filenames = cell(1, length(files));
for i=1:length(files)
	filenames{i} = files(i).name;
end

sims_rec = fopen('sims/sims_300.csv', 'w');

for i=1:length(sims)
	fprintf(sims_rec, '%s, %s, %6f\n', filenames{is(sims_idx(i))}, filenames{js(sims_idx(i))}, sims(i));
end

fclose(sims_rec);