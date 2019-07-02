from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

if __name__ == '__main__':
    img = cv2.imread('pat1.jpg') # Change Image Name Here
    height, width, dim = img.shape

    img = img[int(height/4):int(3*height/4), int(width/4):int(3*width/4), :]
    height, width, dim = img.shape

    img_vec = np.reshape(img, [height * width, dim] )

    kmeans = KMeans(n_clusters=3)
    kmeans.fit( img_vec )

    unique_l, counts_l = np.unique(kmeans.labels_, return_counts=True)
    sort_ix = np.argsort(counts_l)
    sort_ix = sort_ix[::-1]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    x_from = 0.05   
    
    hexs=[]

    for cluster_center in kmeans.cluster_centers_[sort_ix]:
        hex = "%02x%02x%02x" % (int(cluster_center[2]), int(cluster_center[1]), int(cluster_center[0]))
        hexs.append(hex)

        requested_colour = webcolors.hex_to_rgb(u'#'+hex)
        actual_name, closest_name = get_colour_name(requested_colour)

        print("Actual Color:", actual_name, ", Closest Color:", closest_name)
        ax.add_patch(patches.Rectangle( (x_from, 0.05), 0.29, 0.9, alpha=None, facecolor= "#"+hex) )
        x_from = x_from + 0.31
    print("Hex Values : ",hexs)
    plt.show()