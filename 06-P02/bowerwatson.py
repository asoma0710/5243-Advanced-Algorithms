import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def circumcircle(pts):
    (ax,ay),(bx,by),(cx,cy) = pts
    d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    if abs(d)<1e-9:
        return (0,0), np.inf
    ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    return (ux,uy), (ux-ax)**2+(uy-ay)**2

points   = []
triangles = []

fig = plt.figure(figsize=(10,6))
gs = gridspec.GridSpec(1,2,width_ratios=[3,2],wspace=0.4)
ax_mesh = fig.add_subplot(gs[0])
ax_data = fig.add_subplot(gs[1]); ax_data.axis('off')

def redraw(final=True, bad_tris=None, boundary_edges=None):
    ax_mesh.clear()
    ax_mesh.set_xlim(0,1); ax_mesh.set_ylim(0,1); ax_mesh.set_aspect('equal')
    ax_mesh.set_title("Bowyer–Watson Delaunay")
    # plot & label points
    for idx,(x,y) in enumerate(points):
        ax_mesh.scatter(x, y, c='black', s=30, zorder=3)
        ax_mesh.text(x+0.01, y+0.01, str(idx),
                     fontsize=10, color='blue', zorder=4)

    if final:
        for (i,j,k) in triangles:
            tri = np.array([points[i],points[j],points[k],points[i]])
            ax_mesh.plot(tri[:,0],tri[:,1],'k-')
    else:
        # gray out old triangles
        for (i,j,k) in triangles:
            tri = np.array([points[i],points[j],points[k],points[i]])
            ax_mesh.plot(tri[:,0],tri[:,1],color='lightgray')
        # highlight bad triangles in red
        for (i,j,k) in bad_tris:
            tri = np.array([points[i],points[j],points[k],points[i]])
            ax_mesh.plot(tri[:,0],tri[:,1],'r-',linewidth=2)
        # highlight cavity boundary in magenta
        for (u,v) in boundary_edges:
            x0,y0 = points[u]; x1,y1 = points[v]
            ax_mesh.plot([x0,x1],[y0,y1],color='magenta', linewidth=3)
        # draw new triangles in blue
        new_idx = len(points)-1
        for (u,v) in boundary_edges:
            tri = np.array([points[u],points[v],points[new_idx],points[u]])
            ax_mesh.plot(tri[:,0],tri[:,1],'b-',linewidth=2)

    # update the text‐panel
    ax_data.clear(); ax_data.axis('off')
    lines = ["<POINTS>"] + [f"{i}: ({x:.3f}, {y:.3f})"
                             for i,(x,y) in enumerate(points)]
    lines += ["","<TRIANGLES>"] + [f"{ti}: {t}"
                                  for ti,t in enumerate(triangles)]
    ax_data.text(0,1,"\n".join(lines),
                 va='top',family='monospace',fontsize=10)
    plt.pause(0.001)

def onclick(ev):
    if ev.inaxes!=ax_mesh: return
    x,y = ev.xdata, ev.ydata
    points.append((x,y))
    n = len(points)
    # seed initial super‐triangle
    if n==3:
        triangles.append((0,1,2))
        redraw(final=True)
        return

    # find “bad” triangles whose circumcircle contains the new point
    bad = []
    for tri in triangles:
        pts = np.array([points[tri[0]],points[tri[1]],points[tri[2]]])
        center,r2 = circumcircle(pts)
        if (x-center[0])**2 + (y-center[1])**2 < r2:
            bad.append(tri)

    # collect boundary edges of the cavity
    edge_count = {}
    for (i,j,k) in bad:
        for u,v in [(i,j),(j,k),(k,i)]:
            key = tuple(sorted((u,v)))
            edge_count[key] = edge_count.get(key,0) + 1
    boundary = [e for e,c in edge_count.items() if c==1]

    # draw intermediate step
    redraw(final=False, bad_tris=bad, boundary_edges=boundary)
    plt.pause(0.7)

    # remove bad triangles
    for tri in bad:
        triangles.remove(tri)
    # fill hole with new triangles
    new_idx = n-1
    for (u,v) in boundary:
        triangles.append((u,v,new_idx))

    # final redraw
    redraw(final=True)

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
