from scipy.spatial import distance
import matplotlib.pylab as plt

class tile(object):
    "a simple class that parses board objects strings"
    def __init__(self, objectstring):
        tokens = objectstring.split(",")
        self.shape = tokens[1]
        self.color = tokens[2]
        self.is_selected = tokens[7] == 'true'
        self.x = int(float(tokens[8]))
        self.y = int(tokens[9][:-1])

#Function that plots gaze points and objects of the board
def plot_screen(tiles, gazepoints, tolerance=0, filepath=None):
    """ plot an episode screen

    tiles -- a list of tile objects
    gaze points -- a series of sfvec2f objects

    filepath -- optional argument to save the plot to
                a file. The filepath MUST be have a
                valid image extension, e.g. "file.png"
                (bmp, jpg, etc)

    """

    #read gaze points
    gazeX = gazepoints['pixels'].map(lambda x: x.x)
    gazeY = gazepoints['pixels'].map(lambda x: x.y)
    gazeI = gazepoints.index


    #create figure
    fig = plt.figure(figsize=(16,9))
    ax = fig.add_subplot(111)

    ax.set_xlim(-200,2120)
    ax.set_ylim(-200,1280)
    ax.set_ylim(ax.get_ylim()[::-1])
    ax.add_patch(plt.Rectangle((0,0),1920,1080,alpha = 0.05,color = 'b'))
    gax = ax.scatter(gazeX, gazeY, s= 10, c = gazeI, cmap = plt.cm.Reds, label = 'gaze')
    fig.colorbar(gax, format = '%d')

    #draw the objects
    tolerances = []
    for tile in tiles:
        if tile.is_selected:
            ax.text(tile.x, tile.y, tile.shape, size = 'xx-large', weight = 'bold',
                        color = tile.color, bbox=dict(facecolor='red', alpha=0.5))
        else:
            ax.text(tile.x, tile.y, tile.shape, size = 'xx-large', weight = 'bold', color = tile.color)
        #draw the tolerance circles
        circle = plt.Circle((tile.x, tile.y), tolerance, color='r', fill=False)
        ax.add_patch(circle)
    if filepath is not None:
        fig.savefig(filepath, format=filepath.split('.')[1])

#function that plots an episode based on its number
def plot_episode(episodeno,  infos, boards, gazegood, tolerance=0, filepath=None):
    episode_start = int(infos['episodes']['start_time'].ix[episodeno])
    episode_end = int(infos['episodes']['end_time'].ix[episodeno])
    gazeslice = gazegood.ix[episode_start:episode_end]
    boardslice = boards.ix[episode_start:episode_end]
    plot_screen(boardslice.iloc[-1], gazeslice, tolerance, filepath)

#function that returns the board for an episode
def get_board(episodeno,infos, boards): 
    episode_start = int(infos['episodes']['start_time'].ix[episodeno])
    episode_end = int(infos['episodes']['end_time'].ix[episodeno])
    boardslice = boards.ix[episode_start:episode_end]
    return boardslice.iloc[-1]

#function that returns the gaze points for an episode
def get_gaze(episodeno,infos, gazegood): 
    episode_start = int(infos['episodes']['start_time'].ix[episodeno])
    episode_end = int(infos['episodes']['end_time'].ix[episodeno])
    return gazegood.ix[episode_start:episode_end]

#function that gets the number of gaze points on an object
def get_number_of_gaze_points(gazepoints, tile, tolerance):
    count = 0
    for point in gazepoints['pixels']:
        if distance.euclidean((point.x, point.y), (tile.x, tile.y)) < tolerance:
            count += 1
    return count
