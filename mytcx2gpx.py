"""
Class for converting tcx to gpx
"""
import logging
from datetime import datetime
from pathlib import Path

from gpxpy import gpx
from tcxparser import TCXParser
import dateutil.parser
import re

# pylint: disable=logging-format-interpolation


LOGGER = logging.getLogger('tcx2gpx')


class TCX2GPX():
    """
    Convert tcx files to gpx.
    """

    def __init__(self, tcx_path, outdir=None):
        """
        Initialise the class.
        """
        self.tcx_path = Path(tcx_path)
        self.outdir = outdir
        self.tcx = None
        self.track_points = None
        self.gpx = gpx.GPX()

    def convert(self):
        """
        Convert tcx to gpx.
        """
        self.read_tcx()
        self.extract_track_points()
        self.create_gpx()
        self.write_gpx()

    def read_tcx(self):
        """
        Read a TCX file.

        Parameter
        ---------
        tcx_path: str
            Valid path to a TCX file.
        """
        try:
            self.tcx = TCXParser(str(self.tcx_path.resolve()))
            LOGGER.info(
                'Reading                     : {}'.format(self.tcx_path))
        except TypeError as not_pathlib:
            print(not_pathlib)
            raise TypeError('File path did not resolve.')

    def extract_track_points(self):
        """
        Extract and combine features from tcx
        """
        self.track_points = zip(self.tcx.position_values(),
                                self.tcx.altitude_points(),
                                self.tcx.time_values())
        LOGGER.info('Extracting track points from : {}'.format(self.tcx_path))

    def create_gpx(self):
        """
        Create GPX object.
        """
        self.gpx.name = dateutil.parser.parse(
            self.tcx.started_at).strftime('%Y-%m-%d %H:%M:%S')
        self.gpx.description = ''
        gpx_track = gpx.GPXTrack(name=dateutil.parser.parse(self.tcx.started_at).strftime('%Y-%m-%d %H:%M:%S'),
                                 description='')
        gpx_track.type = self.tcx.activity_type
        # gpx_track.extensions = '<topografix:color>c0c0c0</topografix:color>'
        self.gpx.tracks.append(gpx_track)
        gpx_segment = gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        for track_point in self.track_points:
            #pick the right format

            tformat1 = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z$')
            tformat2 = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')
            if tformat1.match(track_point[2]):
                time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            elif tformat2.match(track_point[2]):
                time_format = '%Y-%m-%dT%H:%M:%SZ'
            else:
                print(f'SPATNY FORMAT CASU {track_point[2]}')
            gpx_trackpoint = gpx.GPXTrackPoint(latitude=track_point[0][0],
                                               longitude=track_point[0][1],
                                               elevation=track_point[1],
                                               time=datetime.strptime(track_point[2],
                                                                      time_format))
            gpx_segment.points.append(gpx_trackpoint)
        LOGGER.info('Creating GPX for             : {}'.format(self.tcx_path))

    def write_gpx(self):
        """
        Write GPX object to file.
        """
        out = str(self.tcx_path.resolve()).replace('.tcx', '.gpx')
        with open(out, 'w') as output:
            output.write(self.gpx.to_xml())
        LOGGER.info('GPX written to               : {}'.format(out))
