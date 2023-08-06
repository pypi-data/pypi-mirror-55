from ..test import ExperimentTest, ScanTest, Results
from ..sanity import data
from ..utils import __is_valid_scan__
import json
from . import freesurfer



class HasCorrectItems(freesurfer.HasCorrectItems):
    __doc__ = freesurfer.HasCorrectItems.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00281',
    resource_name = 'FREESURFER6_HIRES'


class HasCorrectFreeSurferVersion(freesurfer.HasCorrectFreeSurferVersion):

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00281',
    resource_name = 'FREESURFER6_HIRES'
    freesurfer_version = 'freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.0-2beb96c'
    __doc__ = freesurfer.HasCorrectFreeSurferVersion.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES') + \
        ' (expected version: %s)'%freesurfer_version


class HasCorrectOSVersion(freesurfer.HasCorrectOSVersion):

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00281',
    resource_name = 'FREESURFER6_HIRES'
    kernel_version = '4.4.120-92.70-default'
    __doc__ = freesurfer.HasCorrectOSVersion.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES') + \
        ' (expected version: %s)'%kernel_version

class IsT1OnlyHippocampalSegmentation(freesurfer.IsT1OnlyHippocampalSegmentation):
    __doc__ = freesurfer.IsT1OnlyHippocampalSegmentation.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00281',
    resource_name = 'FREESURFER6_HIRES'


class IsT2MultispectralHippoSegRunnable(freesurfer.IsT2MultispectralHippoSegRunnable):
    __doc__ = freesurfer.IsT2MultispectralHippoSegRunnable.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00365',
    resource_name = 'FREESURFER6_HIRES'

class IsIRMultispectralHippoSegRunnable(freesurfer.IsIRMultispectralHippoSegRunnable):
    __doc__ = freesurfer.IsIRMultispectralHippoSegRunnable.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00365',
    resource_name = 'FREESURFER6_HIRES'


class IsFreeSurferTimewiseConsistent(freesurfer.IsFreeSurferTimewiseConsistent):
    __doc__ = freesurfer.IsFreeSurferTimewiseConsistent.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00281',
    resource_name = 'FREESURFER6_HIRES'

class ReconAllSnapshot(freesurfer.ReconAllSnapshot):
    __doc__ = freesurfer.ReconAllSnapshot.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00754', # has no FreeSurfer6 resource
    resource_name = 'FREESURFER6_HIRES'


class AreCAVolumesConsistent(freesurfer.AreCAVolumesConsistent):
    __doc__ = freesurfer.AreCAVolumesConsistent.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00281',
    resource_name = 'FREESURFER6_HIRES'

class HasAbnormalAsegFeatures(freesurfer.HasAbnormalAsegFeatures):
    __doc__ = freesurfer.HasAbnormalAsegFeatures.__doc__.replace('FREESURFER6', 'FREESURFER6_HIRES')

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E02443',
    threshold = 7
    resource_name = 'FREESURFER6_HIRES'
