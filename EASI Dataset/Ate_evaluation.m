%% This code is used to evalute the VSLAM results.
%  Find the min ATE for solving the time synchronization issue.

groundtruth = readmatrix("09.txt"); % groundtruth file
result = readmatrix("ut_09.txt"); % estimation result

%% get ATE of the estimated result
[time_dis,e] = find_timeidx(result, groundtruth); % find the minimal ATE

groundtruth(:,1) = groundtruth(:,1) + time_dis;
[~, ref, aligned, error] = slam_ate(groundtruth, result);
ate = mean(error) % ATE

%% plots
camera_traj = groundtruth(:,2:end);
[~, startidx] = find(camera_traj'==ref(:,1));
[~, endidx] = find(camera_traj'==ref(:,end));

figure()
hold on
traj_plot(camera_traj(startidx:endidx,:)');
traj_plot(aligned);
view(45, 45)
legend('ref', 'UFEN')
grid on
axis equal
xlabel("X")
ylabel('Y')
zlabel('Z')


%%  functions
function [t_dis, e] = find_timeidx(data_in, gt) 
% find the minmal ATE
    tstart = -3; % can adjust start/end time to speed up calculation. 
    tend =2;
    t_der = 0.005;
    l=0;
    sam_time = gt(:,1);
    
    for p = tstart:t_der:tend
        l = l + 1;
        t0 = p;  
        gt(:,1) = sam_time + t0;
    
        [t, ref, align, error_ate] = slam_ate(gt, data_in);
        e(l) = mean(error_ate);
    end
    min_e = min(e);
    tidx = find(e==min_e);
    t_dis = tstart + (tidx-1) * t_der;
end



function [times, ref, align_est, error_ate] = slam_ate(gt, result)
% calculate ATE
    gt = gt(:,1:4);
    result = result(:, 1:4);
    result(:,1) = result(:,1) - gt(1,1);
    gt(:,1) = gt(:,1) - gt(1,1);
    matches = time_matches(gt, result);
    times = matches(:, 1)';
    ref = matches(:,2:4)';
    est = matches(:,5:7)';
    [R, s, t] = alignment(matches);
    align_est = s*R*est+ t;

    error_ate = error_summary(ref, align_est);

end

function matches = time_matches(g1, d2)
% find the corresponding time
    thre = 0.02;
    t1 = g1(:,1);
    t2 = d2(:,1);
    j = 1;
    matches = [];
    for i=1:1:length(t2)
        t = t2(i) + 1e-8;
        idx = find(abs(t1-t)<thre);
        if (length(idx)==1)
            matches(j, 1) = t;
            matches(j,2:4) = g1(idx, 2:4);
            matches(j,5:7) = d2(i, 2:4);
            j = j+1;
        end  
        if (length(idx)>1)
            midx = find(abs(t1-t)==min(abs(t1-t)));
            matches(j, 1) = t;
            matches(j,2:4) = g1(midx, 2:4);
            matches(j,5:7) = d2(i, 2:4);
            j = j+1;
        end 
    end
end

function [R, s, t] = alignment(matches)
% trajectory alignment
    d1 = matches(:,2:4);
    d2 = matches(:,5:7);
    dm1 = d1 - mean(d1,1);
    dm2 = d2 - mean(d2,1);
    H = dm1' * dm2;
    [U,D,V] = svd(H');

    if det(U)*det(V)<0
        W = diag([1, 1, -1]);
    else
        W = diag([1, 1, 1]);
    end
    R = (U * W * V')';

    sum = 0;
    for i=1:1:length(dm2)
        norm = dm1(i,:) * dm1(i,:)';
        sum = sum + norm;
    end

    s = sum/trace(D*W);
    t = mean(d1,1)' - s*R*mean(d2,1)';
end

function traj_plot(data)
    data = data';
    x = data(:,1);
    y = -data(:,2);
    z = -data(:,3);
    plot3(x,y,z)
end

function ate_error = error_summary(ref, est)
% ate error
    diff = est - ref;
    ate_error = sqrt(sum(diff.^2));
    Rmse = sqrt((ate_error * ate_error')/length(ate_error));
    Max = max(ate_error);
    Min = min(ate_error);
    Mean = mean(ate_error);  
end