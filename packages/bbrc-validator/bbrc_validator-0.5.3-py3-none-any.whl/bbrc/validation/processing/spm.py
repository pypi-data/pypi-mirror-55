from ..test import ExperimentTest, Results
import os

class HasCorrectNumberOfItems(ExperimentTest):
    '''Passes if a SPM12_SEGMENT resource is found and this resource has the
    correct number of items (i.e. 15).'''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        CORRECT_NUMBER = 15

        files = list(self.xnat_instance.select.experiment(experiment_id).resource('SPM12_SEGMENT').files())

        res = len(files) == CORRECT_NUMBER
        if not res:
            import logging as log
            log.error('%s has %s items (different from %s)'%(experiment_id,
                len(files), CORRECT_NUMBER))

        return Results(res, data=[e.attributes()['Name'] for e in files])


class HasCorrectItems(ExperimentTest):
    '''Passes if a SPM12_SEGMENT resource is found and such resource has the
    main expected items.'''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        from fnmatch import fnmatch

        expected_items = ['rc1*.nii.gz',
                          'rc2*.nii.gz',
                          'c1*.nii.gz',
                          'c2*.nii.gz',
                          'c3*.nii.gz',
                          'c4*.nii.gz',
                          'c5*.nii.gz',
                          'y_*.nii.gz',
                          'iy_*.nii.gz',
                          '*_seg8.mat',
                          'pyscript.m',
                          'pyscript_newsegment.m'
                          ]

        res = self.xnat_instance.select.experiment(experiment_id)\
                .resource('SPM12_SEGMENT')

        file_list = set([e.attributes()['Name'] for e in res.files()])

        for e in expected_items:
            if not [f for f in file_list if fnmatch(f, e)] :
                return Results(False, data=['SPM12Segment %s matching item not found.'%e])

        return Results(True, data=[])


class HasCorrectSPMVersion(ExperimentTest):
    '''This test checks the SPM version used for processing the images.
    Passes if SPM12_SEGMENT outputs were created using the expected version
    (i.e. `SPM v12 Release 7219`).'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00251',

    def run(self, experiment_id):
        if os.environ.get('SKIP_SNAPSHOTS_TESTS'):
            return Results(experiment_id == self.passing[0], data=['Skipping it. (SKIP_SNAPSHOTS_TESTS)'])
        expected_spm_version = 'SPM version: SPM12 Release: 7219'

        data = self.xnat_instance.array.mrsessions(experiment_id=experiment_id,
            columns=['label']).data
        exp_label, project, subject_id = [data[0][e] for e in \
            ['label', 'project', 'xnat:mrsessiondata/subject_id']]

        res = self.xnat_instance.select.project(project).subject(subject_id)\
            .experiment(experiment_id).resource('SPM12_SEGMENT')
        log = res.file('LOGS/%s.log'%exp_label)

        if not log.exists():
            return Results(False, data=['SPM12Segment log file not found.'])

        log_data = self.xnat_instance.get(log.attributes()['URI']).text
        spm_version = [line for line in log_data.splitlines() if line.startswith('SPM version:')]

        if not spm_version or spm_version[0] != expected_spm_version :
            return Results(False, data=['Incorrect SPM version: %s' %spm_version])

        return Results(True, data=[])


class HasCorrectMatlabVersion(ExperimentTest):
    '''This test checks the Matlab version on which SPM package was executed for
    processing the images. Passes if MCR version matches `7.10.0.499` and
    Matlab version matches `R2010a`; fails otherwise.'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00251',

    def run(self, experiment_id):
        from fnmatch import fnmatch

        expected_matlab_version = 'MATLAB Version 7.10.0.499 (R2010a)'

        data = self.xnat_instance.array.mrsessions(experiment_id=experiment_id,
            columns=['label']).data
        exp_label, project, subject_id = [data[0][e] for e in \
            ['label', 'project', 'xnat:mrsessiondata/subject_id']]

        res = self.xnat_instance.select.project(project).subject(subject_id)\
            .experiment(experiment_id).resource('SPM12_SEGMENT')
        log = res.file('LOGS/%s.log'%exp_label)

        if not log.exists():
            return Results(False, data=['SPM12Segment log file not found.'])

        log_data = self.xnat_instance.get(log.attributes()['URI']).text

        matlab_version = [line for line in log_data.splitlines() \
            if line.startswith('MATLAB Version')]
        if not matlab_version or matlab_version[0] != expected_matlab_version :
            return Results(False, data=['Incorrect Matlab version: %s' \
                %matlab_version])

        return Results(True, data=[])

class HasCorrectOSVersion(ExperimentTest):
    '''This test checks the OS version on which SPM12_SEGMENT was executed.
    Passes if OS version matches the expected kernel version (`4.4.120-92.70`);
    fails otherwise.'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00251',

    def run(self, experiment_id):

        expected_kernel_version = 'Operating System: Linux 4.4.120-92.70-default'

        data = self.xnat_instance.array.mrsessions(experiment_id=experiment_id,
            columns=['label']).data
        exp_label, project, subject_id = [data[0][e] for e in \
            ['label', 'project', 'xnat:mrsessiondata/subject_id']]

        res = self.xnat_instance.select.project(project).subject(subject_id)\
            .experiment(experiment_id).resource('SPM12_SEGMENT')
        log = res.file('LOGS/%s.log'%exp_label)

        if not log.exists():
            return Results(False, data=['SPM12Segment log file not found.'])

        log_data = self.xnat_instance.get(log.attributes()['URI']).text
        kernel_version = [line for line in log_data.splitlines() \
            if line.startswith('Operating System:')]

        if not kernel_version or \
                not kernel_version[0].startswith(expected_kernel_version):
            return Results(False, data=['Incorrect OS version: %s' \
                % kernel_version])

        return Results(True, data=[])

class SPM12SegmentSnapshot(ExperimentTest):
    '''This test generates a snapshot of the results generated by SPM12SEGMENT.
    Passes if the snapshot is created successfully. Fails otherwise. Does not
    tell anything on the segmentation quality. '''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00754',

    def run(self, experiment_id):
        import tempfile
        if os.environ.get('SKIP_SNAPSHOTS_TESTS'):
            return Results(experiment_id == self.passing[0],
                data=['Skipping it. (SKIP_SNAPSHOTS_TESTS)'])
                
        from ..sanity import data
        p = data.HasPreferredT1(self.lut, self.xnat_instance)
        e = p.preferred_T1(experiment_id)

        resources_files = list(self.xnat_instance.select.experiment(experiment_id)\
                .scan(e).resource('NIFTI').files())

        if len(resources_files) == 0:
            return Results(False, data=['T1 not found.'])

        for f in resources_files:
            if f.label().endswith('.nii.gz'):
                break

        _, path = tempfile.mkstemp(suffix='.nii.gz')
        f.get(dest=path)
        t1_fp = path

        resources_files = list(self.xnat_instance.select.experiment(experiment_id)\
                .resource('SPM12_SEGMENT').files())

        if len(resources_files) == 0:
            return Results(False, data=['SPM results not found.'])

        for f in resources_files:
            if f.label().startswith('c1'):
                break

        if not f.label().startswith('c1'):
            return Results(False, data=['c1 map (SPM) not found.'])

        _, c1_fp = tempfile.mkstemp(suffix='.nii.gz')
        f.get(dest=c1_fp)

        from . import probamap_snapshot
        paths = probamap_snapshot(t1_fp, c1_fp)

        return Results(True, data=paths)

    def report(self):
        report = []

        for path in self.results.data:
            report.append('![snapshot](%s)'%path)
        return report


class HasNormalSPM12Volumes(ExperimentTest):
    '''This test runs the quality-predicting procedure on the SPM12SEGMENT resource
    based on its estimated gray and white matter volumes estimated by SPM12.
    Test passes if volumes are within boundaries, i.e. `gray matter` volume ranges
    between 480000 and 900000; `white matter` volume ranges between 300000 and 600000).
    Test fails otherwise.'''

    passing = 'BBRCDEV_E00559',
    failing = 'BBRCDEV_E01613',

    def check(self, vols):
        boundaries = [('c1', [480000, 900000]),
                      ('c2', [300000, 600000])]
        has_passed = True

        for (col, (bmin, bmax)), subject_val  in zip(boundaries, vols[:2]):
            if float(subject_val) > float(bmax) or float(subject_val) < float(bmin):
                has_passed = False
        return has_passed

    def run(self, experiment_id):
        import tempfile
        import nibabel as nib
        import numpy as np

        r = self.xnat_instance.select.experiment(experiment_id).resource('SPM12_SEGMENT')
        if not r.exists():
            return Results(False, data=['Missing SPM12_SEGMENT resource'])
        vols = []
        _, fp = tempfile.mkstemp(suffix='.nii.gz')

        for kls in ['c1', 'c2', 'c3']:
            f = [each for each in r.files() if each.id().startswith(kls)][0]
            f.get(fp)
            d = nib.load(fp)
            size = np.prod(d.header['pixdim'].tolist()[:4])
            v = np.sum(d.dataobj) * size
            vols.append(v)

        res = self.check(vols)
        return Results(res, data=['Volumes: %s %s'%(vols[0], vols[1])])


class SPM12SegmentExecutionTime(ExperimentTest):
    '''This test checks the execution time of `SPM12 Segment` in the log files.
    The test passes if elapsed time is within an acceptable range of 5 to 30
    minutes; fails otherwise.'''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E01613',

    def get_spm_log(self,experiment_id):
        from fnmatch import fnmatch

        match_string = '%s.log' % self.xnat_instance.select.experiment(experiment_id).label()

        # get metadata for each Experiment's scan
        uri = '/data/experiments/' + experiment_id + '/resources/SPM12_SEGMENT/files'
        data = self.xnat_instance._get_json(uri)

        return [item['URI'] for item in data if fnmatch(item['Name'], match_string)]

    def run(self,experiment_id):
        import re
        import dateparser
        import datetime

        uris = self.get_spm_log(experiment_id)
        if len(uris) != 1:
            return Results(False, data=['No SPM12_Segment log files found.'])

        log_data = self.xnat_instance.get(uris[0]).text.strip()

        start_end_tags = ['SPM12: spm_preproc_run',
                          'Completed                               :']
        dates = []
        for tag in start_end_tags :
            for line in log_data.splitlines():
                if line.startswith(tag):
                    time, _, date = re.split(r'\s+', line)[-3:]
                    dates.append(dateparser.parse(date + ' ' + time))
                    break

        if len(dates) != 2:
            return Results(False, data=['Invalid SPM12_Segment log file.'])

        result = False
        tdelta = max(dates) - min(dates)
        if tdelta > datetime.timedelta(minutes=5) and\
           tdelta < datetime.timedelta(minutes=30) :
            result = True

        return Results(result, data=['%s' % tdelta])
