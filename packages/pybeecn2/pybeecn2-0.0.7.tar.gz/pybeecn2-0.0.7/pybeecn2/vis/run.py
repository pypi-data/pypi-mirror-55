
import os
import shutil
import logging.config
import folium
import numpy as np
import geopandas as gpd
logger = logging.getLogger(__name__)


def setup_analysis_directory(directory):
    directory = os.path.abspath(directory)
    dirs = dict(
        plots=os.path.join(directory, 'plot_files'),
        data=os.path.join(directory, 'data_files'),
        geo=os.path.join(directory, 'geo_files'),
        report=os.path.join(directory, 'final_report')
    )

    # Creating New Analysis Directory (if required)
    if not os.path.exists(directory):
        logger.info("Creating New Analysis Directory: {}".format(directory))
        os.makedirs(directory)

    # Creating Sub directories
    for name, d in dirs.items():
        if not os.path.exists(d):
            logger.info("Creating Analysis {} Directory: {}".format(name, d))
            os.makedirs(d)

    return dirs


def get_map_data(url: str):
    points_data = gpd.read_file(url)
    return points_data


def make_locations(points: gpd.geoseries.GeoSeries):
    latitudes = []
    longitudes = []
    for pnt in points:
        tmp = str(pnt).lstrip('POINT (').rstrip(')')
        long, lat = tmp.split(' ')
        latitudes.append(float(lat))
        longitudes.append(float(long))
    points = []
    for lat, long in zip(latitudes, longitudes):
        points.append((lat, long))
    return points


def get_map_center(points: list):
    lats = [pnt[0] for pnt in points]
    longs = [pnt[1] for pnt in points]
    lat_ave = np.array(lats).mean()
    long_ave = np.array(longs).mean()
    return lat_ave, long_ave


def create_map(latitude: float, longitude: float):
    m = folium.Map(location=[latitude, longitude], zoom_start=11.5)
    return m


def make_choropleth(boundary_data, demographic):
    if 'Total' in demographic:
        show = True
    else:
        show = False
    population = folium.Choropleth(
                   geo_data=boundary_data,
                   data=boundary_data,
                   columns=['OBJECTID', demographic],
                   key_on='feature.properties.OBJECTID',
                   fill_color='YlGn',
                   fill_opacity=0.6,
                   line_opacity=0.2,
                   legend_name='{} Population Size by Tract'.format(demographic),
                   highlight=True,
                   name='{} Population'.format(demographic),
                   show=show)
    return population


def make_feature_points(points: list, point_names: list, addresses: list, layer_name=None):
    fg = folium.FeatureGroup(name=layer_name)
    for pnt, nm, add in zip(points, point_names, addresses):
        tooltip = '<b>Name</b>: {} <br>' \
                  '<b>Address</b>: {} <br>'.format(nm, add)
        folium.Marker(pnt, tooltip=tooltip).add_to(fg)
    return fg


def make_point_rings(points: list, layer_name='Ring', radius=1600):
    fg = folium.FeatureGroup(name=str(radius) + ' ' + layer_name)
    for pnt in points:
        folium.Circle(pnt, weight=1.5, radius=radius).add_to(fg)
    return fg


# def get_boundary(fg: folium.map.FeatureGroup):
#     json = fg.to_json()


def main(args):
    """
    :param args:
    :return:
    """

    demographics = ['Total_Pop_5_n_over', 'Spanish', 'Russian', 'Other_Slavic', 'Other_Indic',
                    'Other_Indo_European', 'Chinese', 'Japanese', 'Korean', 'Mon_Khmer_Cambodian',
                    'Laotian', 'Vietnamese', 'Other_Asian', 'Tagalog', 'Other_Pacific_Island',
                    'Arabic', 'African']

    # Setup plot directory
    # -----------------------------------------------------------------------------------------------------------------
    directory = os.path.join(args.directory, 'beecn')

    # Setup the directory
    # -----------------------------------------------------------------------------------------------------------------
    dirs = setup_analysis_directory(directory)

    if len(os.listdir(dirs["plots"])) != 0:
        logger.warning("Plots Directory: {} is not empty...removing old plots".format(os.path.join(dirs['plots'])))
        shutil.rmtree(dirs["plots"])
        os.makedirs(dirs["plots"])

    if len(os.listdir(dirs["data"])) != 0:
        logger.warning("Data Directory: {} is not empty...removing old files".format(os.path.join(dirs['data'])))
        shutil.rmtree(dirs["data"])
        os.makedirs(dirs["data"])

    # Get the data
    # -----------------------------------------------------------------------------------------------------------------
    logger.info('Getting the boundary data from {}'.format(args.boundaries))
    boundary_data = get_map_data(args.boundaries)
    logger.info('Points data...{}'.format(boundary_data))

    logger.info('Getting the point data from {}'.format(args.points))
    points_data = get_map_data(args.points)
    logger.info('Points data...{}'.format(points_data))

    # Start building the map
    # -----------------------------------------------------------------------------------------------------------------
    beecn_points = make_locations(points_data.geometry)
    lat, long = get_map_center(points=beecn_points)
    m = create_map(latitude=lat, longitude=long)
    for dem in enumerate(demographics):
        logger.info('Making map layer for {}'.format(demographics[dem[0]]))
        population = make_choropleth(boundary_data, demographics[dem[0]]).add_to(m)
        if dem[0] == 0:
            field = demographics
        else:
            field = [demographics[0], demographics[dem[0]]]
        folium.GeoJson(boundary_data,
                       tooltip=folium.features.GeoJsonTooltip(fields=field,
                                                              localize=True,
                                                              sticky=True),
                       smooth_factor=0.0
                       ).add_to(population.geojson)
        for key in population._children.keys():
            if 'color_map' in key:
                del(population._children[key])
    been_fg = make_feature_points(beecn_points, points_data.SITE_NAME, points_data.LOCATION,
                                  layer_name='BEECN Sites').add_to(m)
    radius_fg = make_point_rings(beecn_points).add_to(m)

    m.add_child(folium.LayerControl())

    fname = os.path.join(dirs['plots'], 'population_map_center_{}_{}.html'.format(lat, long))
    logger.info('Saving the map: {}'.format(fname))
    m.save(fname)
