# Imports
import matplotlib.pyplot as plt
import numpy as np
from plicp_cov import PLICP, KalmanICPCov
import graph_constructor
import g2o
import csv
import scipy
import ast
import atexit
import imageio
from plot_g2o import *
import time

# File path
file_path = "../data_store/mapping/26-05|16:54:06.csv" #diamond
# file_path = "../data_store/mapping/22-05|12:07:08.csv" #rectangular
# file_path = "../data_store/mapping/22-05|10:06:54.csv" #room


def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

pose = []
angle_min = []
angle_max = []
angle_increment = []
range_min = []
range_max = []
ranges = []
intensities = []
lasers = []

print(" ---- Start Extracted ----")
with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for i, row in enumerate(csv_reader):
        pose_value = ast.literal_eval(row['pose'])
        pose_list = list(pose_value) 
        pose.append(pose_list)

        angle_min.append(float(row['angle_min']))
        angle_max.append(float(row['angle_max']))
        angle_increment.append(float(row['angle_increment']))
        range_min.append(float(row['range_min']))
        range_max.append(float(row['range_max']))

        ranges.append(np.array([float(x) for x in row['ranges'].strip('[]').split(',')]))

odoms = np.array(pose)
angle_min = np.array(angle_min)
angle_max = np.array(angle_max)
angle_increment = np.array(angle_increment)
range_min = np.array(range_min)
range_max = np.array(range_max)

for i in range(len(ranges)):
    temp = []
    for j in range(len(ranges[i])):
        if range_min[i] < ranges[i][j] < range_max[i]:
            angle = angle_min[i] + (j * angle_increment[i])
            x, y = polar_to_cartesian(ranges[i][j], angle)
            temp.append(np.array([x, y]))
    lasers.append(temp)

print(" ---- Done Extracted ---- ")

start = time.time()
dx_diff = 0.05
dx_theta = 0.05
lc_mod = 10
length = len(odoms)
closure = 0.05

filename = f'../output_graph/slam_{dx_diff}_{dx_theta}_{lc_mod}_{length}_{closure}_dist:0.1_unbounded'
images = []
atexit.register(lambda: imageio.mimsave(
    filename+".gif",
    images, fps=10))

plicp = PLICP()
icp_cov = KalmanICPCov()

optimizer = graph_constructor.PoseGraphOptimization()
pose = np.eye(3)
optimizer.add_vertex(0, g2o.SE2(g2o.Isometry2d(pose)), True)

init_pose = np.eye(3)
vertex_idx = 1
registered_lasers = []

max_x = -float('inf')
max_y = -float('inf')
min_x = float('inf')
min_y = float('inf')

loop_closures = []
odom_idx_vertex = []

for odom_idx, odom in enumerate(odoms[:length]):
    if odom_idx == 0:
        prev_odom = odom.copy()
        prev_idx = 0
        src = lasers[odom_idx]
        registered_lasers.append(src)
        continue

    dx = odom - prev_odom
    if np.linalg.norm(dx[0:2]) > dx_diff or abs(dx[2]) > dx_theta:
        ref = np.array(lasers[prev_idx])
        src = np.array(lasers[odom_idx])

        init_pose = np.array([[dx[0]], [dx[1]], [dx[2]]])
        state, corresp, src_latest, _ = plicp.run(src.T, ref.T)
        cov_icp = icp_cov.run(src.T, ref.T, plicp.rot(state[2]), state[:2], corresp)
        T = plicp.homogeneous_transform(state)
       
        init_pose = state
        pose = np.matmul(pose, T)
        optimizer.add_vertex(vertex_idx, g2o.SE2(g2o.Isometry2d(pose)))

        rk = g2o.RobustKernelHuber()
        information = np.linalg.inv(cov_icp)
        optimizer.add_edge([vertex_idx-1, vertex_idx],
                           g2o.SE2(g2o.Isometry2d(T)),
                           information, robust_kernel=rk)
        
        prev_odom = odom
        prev_idx = odom_idx
        registered_lasers.append(src)
        odom_idx_vertex.append((odom_idx, vertex_idx))

        if vertex_idx > 6 and not vertex_idx % lc_mod:
            poses = [optimizer.get_pose(idx).to_vector()[0:-1]
                     for idx in range(vertex_idx-1)]
            kd = scipy.spatial.cKDTree(poses)
            x, y, theta = optimizer.get_pose(vertex_idx).to_vector()
            direction = np.array([np.cos(theta), np.sin(theta)])
            idxs = kd.query_ball_point(np.array([x, y]), r=1)
            for idx in idxs:
                ref = np.array(registered_lasers[idx])
                with np.errstate(all='raise'):
                    state, corresp, _, dist = plicp.run(src.T, ref.T)
                    cov_icp = np.eye(3)
                    T = plicp.homogeneous_transform(state)
                information = np.linalg.inv(cov_icp)
                if np.mean(dist) < closure:
                    print("Loop Closure !!!")
                    loop_closures.append((vertex_idx, idx))
                    rk = g2o.RobustKernelDCS()
                    optimizer.add_edge([vertex_idx, idx],
                                       g2o.SE2(g2o.Isometry2d(T)),
                                       information, robust_kernel=rk)
            optimizer.optimize()
        pose = optimizer.get_pose(vertex_idx).to_isometry().matrix()

        traj = np.empty((0, 2))
        point_cloud_list = []
        draw_last = float('inf')

        for idx in range(max(0, vertex_idx - draw_last), vertex_idx):
            x = optimizer.get_pose(idx)
            r = x.to_isometry().R
            t = x.to_isometry().t
            filtered = np.array(registered_lasers[idx])
            filtered = filtered[np.linalg.norm(filtered, axis=1) < 50]
            point_cloud_list.append(np.matmul(filtered, r.T) + t)
            traj = np.vstack([traj, x.to_vector()[0:2]])
        
        point_cloud = np.vstack(point_cloud_list)

        xyreso = 0.05
        point_cloud = (point_cloud / xyreso).astype('float')
        point_cloud = np.unique(point_cloud, axis=0)
        point_cloud = point_cloud * xyreso

        current_max = np.max(point_cloud, axis=0)
        current_min = np.min(point_cloud, axis=0)
        max_x = max(max_x, current_max[0])
        max_y = max(max_y, current_max[1])
        min_x = min(min_x, current_min[0])
        min_y = min(min_y, current_min[1])

        plt.cla()
        plt.axis([min_x, max_x, min_y, max_y])

        traj = np.array(traj)
        plt.plot(traj[:, 0], traj[:, 1], '-b')
        plt.plot(point_cloud[:, 0], point_cloud[:, 1], '.r', markersize=0.1)
        plt.axis("off")
        plt.pause(0.001)
        plt.gcf().canvas.draw()

        image = np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype='uint8')
        image  = image.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
        images.append(image)
        vertex_idx += 1

# Plot loop closures
end = time.time()
print(f"Runtime : {start-end} seconds")

# Plot the final result
plt.figure()
plt.axis([min_x, max_x, min_y, max_y])
traj = np.array(traj)
plt.plot(traj[:, 0], traj[:, 1], '-b')
plt.plot(point_cloud[:, 0], point_cloud[:, 1], '.r', markersize=0.1)

x = []
y = []

# for lc in loop_closures:
#     start_idx = odom_idx_vertex[lc[0]][0]
#     end_idx = odom_idx_vertex[lc[1]][0]
#     x.append(odoms[start_idx][0])
#     y.append(odoms[start_idx][1])
#     x.append(odoms[end_idx][0])
#     y.append(odoms[end_idx][1])
#     plt.plot([odoms[start_idx][0], odoms[end_idx][0]],
#              [odoms[start_idx][1], odoms[end_idx][1]], 'r--', linewidth=2)

# plt.scatter(np.array(x), np.array(y))
# plt.title("Loop Closure Pose", fontsize=20)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.axis("on")
# plt.show()

print(len(traj), len(point_cloud_list))
with open(filename+".csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['poses', 'pointclouds'])
    for i in range(len(traj)):
        writer.writerow([traj[i].tolist(), point_cloud_list[i].tolist()])

fig = plot_slam2d(optimizer, "Posisi Hasil dari PGO")