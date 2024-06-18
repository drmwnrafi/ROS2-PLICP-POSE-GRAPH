import matplotlib.pyplot as plt
import g2o

def plot_slam2d(optimizer, title):
    def edges_coord(edges, dim):
        for e in edges:
            yield e.vertices()[0].estimate()[dim]
            yield e.vertices()[1].estimate()[dim]
            yield None

    fig, ax = plt.subplots()

    # edges
    edges = optimizer.edges()  # get set once to have same order
    se2_edges = [e for e in edges if type(e) == g2o.EdgeSE2]
    se2_pointxy_edges = [e for e in edges if type(e) == g2o.EdgeSE2PointXY]

    # Plot SE2PointXY edges
    for e in se2_pointxy_edges:
        x_coords = list(edges_coord([e], 0))
        y_coords = list(edges_coord([e], 1))
        ax.plot(x_coords, y_coords, linestyle='--', color='firebrick', linewidth=1, label='Measurement edges')
    
    # Plot SE2 edges
    for e in se2_edges:
        x_coords = list(edges_coord([e], 0))
        y_coords = list(edges_coord([e], 1))
        ax.plot(x_coords, y_coords, linestyle='-', color='midnightblue', linewidth=1, label='Pose edges')

    # Remove duplicate labels in the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    # poses of the vertices
    vertices = optimizer.vertices()
    poses = [v.estimate() for v in vertices.values() if type(v) == g2o.VertexSE2]
    measurements = [v.estimate() for v in vertices.values() if type(v) == g2o.VertexPointXY]

    # Plot poses
    ax.scatter([v[0] for v in poses], [v[1] for v in poses], c='lightskyblue', edgecolor='midnightblue', s=50, label='Poses')

    # Plot measurements
    ax.scatter([v[0] for v in measurements], [v[1] for v in measurements], c='firebrick', marker='*', s=150, label='Measurements')

    ax.set_aspect('equal')
    ax.set_title(title, fontsize=20)

    plt.show()