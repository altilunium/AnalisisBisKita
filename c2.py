import gpxpy
import shapefile

def convert_gpx_to_shp(gpx_file, shp_file):
    # Create a new Shapefile
    shp_writer = shapefile.Writer(shp_file)
    shp_writer.autoBalance = 1

    # Define the Shapefile fields
    shp_writer.field('AverageSpeed', 'F', 10, 6)
    shp_writer.field('Timestamp', 'C', 30)

    # Load the GPX file
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)

    # Iterate over each track in the GPX file
    for track in gpx.tracks:
        # Iterate over each segment in the track
        for segment in track.segments:
            # Iterate over each point in the segment
            for i, point in enumerate(segment.points):
                # Calculate the average speed
                if i > 0:
                    distance = point.distance_2d(segment.points[i-1])
                    time_diff = point.time - segment.points[i-1].time
                    speed_mps = distance / time_diff.total_seconds()
                    speed_kmph = speed_mps * 3.6  # Convert m/s to km/h
                    timestamp = point.time.strftime('%Y-%m-%d %H:%M:%S')
                    shp_writer.point(point.longitude, point.latitude)
                    shp_writer.record(speed_kmph, timestamp)

    # Save the Shapefile
    shp_writer.close()

# Usage example
gpx_file = 'vida.gpx'
shp_file = 'vida.shp'
convert_gpx_to_shp(gpx_file, shp_file)