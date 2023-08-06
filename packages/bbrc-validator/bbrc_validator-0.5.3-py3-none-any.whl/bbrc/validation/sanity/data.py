from ..test import ExperimentTest, ScanTest, Results
from ..utils import __is_valid_scan__
from six import string_types

import urllib
import json
try:
    unicode
except NameError:
    unicode = str

class IsEven(ExperimentTest):
    ''' Returns True if the experiment_id is an even number, False if odd. '''

    passing = '030423270818090',
    failing = '030423270818091',

    def run(self, experiment_id):
        sid = int(experiment_id)
        res = (sid % 2 == 0)
        return Results(res)


class HasDuplicatedSequence(ScanTest):
    '''Every sequence should have a unique identifier (SeriesNumber).
    Fails if another scan exists with the same name. Passes if unique.
    Returns sequences (SeriesNumber) sharing an identical `scan-type` or
    scanning procedure definition.'''

    passing = 'BBRCDEV_E00007', '401'
    failing = 'BBRCDEV_E00007', '1401'

    def run(self, experiment_id, scan_id):
        # get metadata for each Experiment's scan
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=['xnat:imageScanData/quality',
                                                        'xnat:imageScanData/type',
                                                        'xsiType']
                                               ).data
        scans = {s['xnat:imagescandata/id']:s for s in scans}
        scan_type = scans[scan_id]['xnat:imagescandata/type']

        # filter out unsuitable scan items
        valid_scans = {str(scan): scans[scan] for scan in scans
            if __is_valid_scan__(self.xnat_instance, scans[scan])}

        # check occurrences of scans of type 'scan_type'
        import fnmatch
        matching_scans = [scan for scan in valid_scans
            if fnmatch.fnmatch(valid_scans[scan]['xnat:imagescandata/type'], scan_type)]

        res = (len(matching_scans) == 1)
        data = {scan_type : matching_scans} if not res else None
        return Results(res, data=[data])


class HasDuplicatedSequences(ExperimentTest):
    '''Every sequence should have a unique identifier (SeriesNumber).
    Fails if multiple scans have an identical `scan-type` or scanning procedure
    definition with the same name. Passes if `scan-type`s are unique.
    Returns sequences (SeriesNumber) sharing an identical `scan-type`.'''

    passing = 'BBRCDEV_E00281',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):

        # get metadata for each Experiment's scan
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=['xnat:imageScanData/quality',
                                                        'xnat:imageScanData/type',
                                                        'xnat:imageScanData/frames',
                                                        'xsiType']
                                               ).data
        scans = {s['xnat:imagescandata/id']:s for s in scans}

        # filter out unsuitable scan items
        valid_scans = {str(scan): scans[scan] for scan in scans
            if __is_valid_scan__(self.xnat_instance, scans[scan])}
        scan_types = [valid_scans[e]['xnat:imagescandata/type'] for e, _ in valid_scans.items()]

         # check occurrences of scans of type 'scan_type'
        import fnmatch
        n_scans = {}
        for t in scan_types:
            n_scans[t] = [s_id for s_id, s_res in valid_scans.items()
                if fnmatch.fnmatch(s_res['xnat:imagescandata/type'], t)]

        res = not False in [(len(ns) == 1) for ns in n_scans.values()]
        data = dict([(k, n) for k, n in n_scans.items() if len(n)!=1]) \
            if not res else {}
        return Results(res, data=data)

    def report(self):
        report = []
        for k, v in self.results.data.items():
            report.append('%s : %s<br>'%(k,', '.join(v)))
        return report


class HasThumbnails(ScanTest):
    '''Most datasets should have snapshots available for previewing if imaging data is valid. Note however that snapshot generation
    is disabled for 'complex' sequences such as fMRI,DWI and DTI (known XNAT behaviour). Test skipped if scan in excluded list.
    Test passes if snapshots exist. Fails if missing.'''

    passing = 'BBRCDEV_E00272', '301'
    failing = 'BBRCDEV_E00013', '301'

    def run(self, experiment_id, scan_id):

        resource_label = 'SNAPSHOTS'
        excluded_scans = self.lut.get('DWI', []) +\
                         self.lut.get('RS', [])

        # check scan type/description against excluded list
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns = ['ID',
                                                          'xnat:imageScanData/type']
                                               ).data
        scans = {s['xnat:imagescandata/id']:s for s in scans}

        if scans[scan_id]['xnat:imagescandata/type'] in excluded_scans :
            msg = 'No thumbnails for `%s` scans (known bug). Skipping scan %s.' \
                %(scans[scan_id]['xnat:imagescandata/type'],scan_id)
            return Results(None, data=[msg])

        # get resources' metadata for given scan
        scan = self.xnat_instance.select.experiment(experiment_id).scan(scan_id)
        uri = scan._uri + '/resources'
        resources = {e['xnat_abstractresource_id']: e for e in self.xnat_instance._get_json(uri)}

        # filter suitable resources based on SNAPSHOTS resource content & label
        matching_resources = [resources[res_id] for res_id in resources
                                   if resources[res_id]['content'] == resource_label
                                   and resources[res_id]['label'] == resource_label
                                   and resources[res_id]['file_count']
                                   and int(resources[res_id]['file_count']) > 0 ]

        res = (len(matching_resources) >= 1)
        return Results(res)


class HasNifti(ScanTest):
    '''Datasets are automatically converted to NIfTI (depends on projects).
    Passes if the sequence has an existing NIfTi version. Fails if NIfTI is
    missing.'''

    passing = 'BBRCDEV_E00007', '301'
    failing = 'BBRCDEV_E00021', '101'

    def run(self, experiment_id, scan_id):

        resource_label = 'NIFTI'
        resource_content = 'NIFTI_RAW'

        # get resources' metadata for given scan
        scan = self.xnat_instance.select.experiment(experiment_id).scan(scan_id)
        uri = scan._uri + '/resources'
        resources = {e['xnat_abstractresource_id']: e for e in self.xnat_instance._get_json(uri)}

        # filter suitable resources based on NIFTI resource content & resource label
        matching_resources = [resources[res_id] for res_id in resources
                                   if resources[res_id]['content'] == resource_content
                                   and resources[res_id]['label'] == resource_label
                                   and resources[res_id]['file_count']
                                   and int(resources[res_id]['file_count']) > 0 ]

        res = (len(matching_resources) >= 1)
        return Results(res)


class HasUncompressedPixelData(ScanTest):
    '''Passes if the Pixel Data portion of the DICOM dataset is uncompressed.
    Fails otherwise.'''

    passing = 'BBRCDEV_E00272', '301'
    failing = 'BBRCDEV_E00013', '301'

    def run(self, experiment_id, scan_id):

        from pydicom.uid import UncompressedPixelTransferSyntaxes

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID',
                                                               'subject_label']
                                                      ).data[0]
        project_id = labels['project']

        # compose the URL for the XNAT dicomdump service
        uri = '/data/services/dicomdump'
        options = {'src': '/archive/projects/%s/experiments/%s/scans/%s'\
                        % (project_id, experiment_id, scan_id),
                   'field': 'TransferSyntaxUID',
                   'format': 'csv'
                   }
        from pyxnat.core.jsonutil import csv_to_json
        transfer_syntax_tags = csv_to_json(unicode(self.xnat_instance.get(uri, params=options).text))

        # Transfer Syntax UID tag MUST be unique and mandatorily present (DICOM
        # standard compliance)
        if not len(transfer_syntax_tags) == 1:
            return Results(None,
                {'info' : 'Transfer Syntax UID tag MUST be unique and '
                          'mandatorily present'})
        transfer_syntax_uid = transfer_syntax_tags[0]

        res = (transfer_syntax_uid['value'] in UncompressedPixelTransferSyntaxes)
        return Results(res)


class IsClassicDICOM(ScanTest):
    '''Every dataset should be uploaded to XNAT using the classic DICOM format.
    Passes if the scan is stored in classic DICOM. Fails if stored in
    enhanced DICOM.'''

    passing = 'BBRCDEV_E00272', '301'
    failing = 'BBRCDEV_E00007', '301'

    def run(self, experiment_id, scan_id):

        ENHANCED_MR_IMAGE_SOPS = \
            {'1.2.840.10008.5.1.4.1.1.4.1': 'Enhanced MR Image Storage',
             '1.2.840.10008.5.1.4.1.1.4.3': 'Enhanced MR Color Image Storage',
             '1.2.840.10008.5.1.4.1.1.4.4': 'Legacy Converted Enhanced MR Image Storage'}

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID']
                                                      ).data[0]
        project_id = labels['project']

        # compose the URL for the XNAT dicomdump service
        uri = '/data/services/dicomdump'
        options = {'src': '/archive/projects/%s/experiments/%s/scans/%s' \
            % (project_id, experiment_id, scan_id),
                   'field': 'MediaStorageSOPClassUID',
                   'format': 'csv'}

        from pyxnat.core.jsonutil import csv_to_json
        sopclass_tags = csv_to_json(unicode(self.xnat_instance.get(uri, params=options).text))


        # SOPClass UID tag MUST be unique and mandatorily present (DICOM standard compliance)
        if len(sopclass_tags) != 1 :
            import logging as log
            log.error('Wrong SOPClassUID(s): %s'%sopclass_tags)
            return Results(False, data=['Unknown SOPClassUID %s'%sopclass_tags])

        sopclass_uid = sopclass_tags[0]

        res = (sopclass_uid['value'] not in ENHANCED_MR_IMAGE_SOPS.keys())
        return Results(res)


class HasPhilipsPrivateTags(ScanTest):
    ''' Passes if the dataset has Philips private tags stored in the DICOM
    header. Fails otherwise.'''

    passing = 'BBRCDEV_E00014', '1501'
    failing = 'BBRCDEV_E00010', '1301'

    def run(self, experiment_id, scan_id):


        # pick a threshold based on observation to determine whether an study
        #has all Private groups info or it was emptied
        EMPTY_GROUPS_MIN_TAG_LENGTH = (40, 80)

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID']
                                                      ).data[0]
        project_id = labels['project']

        # compose the URL for the XNAT dicomdump service
        uri = '/data/services/dicomdump'
        options = {'src': '/archive/projects/%s/experiments/%s/scans/%s' \
                % (project_id, experiment_id, scan_id),
                   'format': 'csv'}

        from pyxnat.core.jsonutil import csv_to_json
        ans = self.xnat_instance.get(uri, params=options).text
        dicomdump_list = csv_to_json(unicode(ans).encode('utf-8'))

        philips_private_2001 = [item for item in dicomdump_list if '(2001,' in str(item['tag1'])]
        philips_private_2005 = [item for item in dicomdump_list if '(2005,' in str(item['tag1'])]

        res = (len(philips_private_2001), len(philips_private_2005)) > EMPTY_GROUPS_MIN_TAG_LENGTH
        return Results(res)


class HasBvecBval(ScanTest):
    '''Diffusion-weighted datasets should have a BVEC and a BVAL file generated
    by the conversion to NIfTI. Passes if the dataset has existing and
    non-empty BVEC and BVAL items. Fails otherwise.'''

    passing = 'BBRCDEV_E00014', '1501'
    failing = 'BBRCDEV_E00015', '1301'

    def get_bvec_bval_data(self, uris):
        '''Helper that given a set or URIs of bvev,bval files return
        diffusion BVEC and BVAL files content as numpy n-dimensional array types.'''

        import re
        import numpy as np

        bvecbval_data = {}
        for k,v in uris.items():
            content = self.xnat_instance.get(v).text
            # parse tab-separated string items as a list
            str_matrix =  [re.split(r'\s+', s.rstrip(r'\s')) for s in content.splitlines()]
            # convert into a numpy array
            ndarray_item = np.asarray(str_matrix)
            # cast numpy array values into floats (from string)
            ndarray_item = ndarray_item.astype(float)

            bvecbval_data[k] = ndarray_item

        return bvecbval_data

    def run(self, experiment_id, scan_id):
        import os.path as op

        resource_label = 'NIFTI'
        valid_extensions = ['.bvec','.bval']
        result = False
        data = None

        # pick a threshold based on observation to determine whether a bvec/bval
        # file size (Bytes) represents a valid file
        BVECBVAL_MIN_FILESIZE = 50

        # get resources' files info for given scan
        uri = '/data/experiments/%s/scans/%s/resources/%s/files'\
            % (experiment_id, scan_id, resource_label)

        files_list = self.xnat_instance._get_json(uri)

        # exclude from valid BVEC/BVAL file candidates those without a proper
        # extension AND smaller than 50Byte size
        bvecbval_files_info = { op.splitext(current['Name'])[1] : current['URI']
                                for current in files_list
                                if op.splitext(current['Name'])[1] in valid_extensions
                                and int(current['Size']) > BVECBVAL_MIN_FILESIZE }

        # check that the bvec file contains as many vectors as the bval has values
        try:
            bvec_bval_content = self.get_bvec_bval_data(bvecbval_files_info)
        except ValueError as e:
            import logging as log
            log.error('%s'%e)
            data = ['Exception: %s'%e]
            bvec_bval_content = {}
        sizes = [ item.shape[1] for item in bvec_bval_content.values() ]

        # list should contain exactly a pair of file items (bvec and bval)
        res = len(bvecbval_files_info) == 2 and \
              len(set(sizes)) == 1 and \
            set(valid_extensions).issubset(set(bvecbval_files_info.keys()))
        return Results(res, data=data)


class HasBvecBvalInDWIScans(ExperimentTest):
    '''Diffusion-weighted datasets should have a BVEC and a BVAL file generated
    by the conversion to NIfTI. Passes if the dataset has existing and
    non-empty BVEC and BVAL items or simply no DWI/DTI scans included. Fails otherwise.'''

    passing = 'BBRCDEV_E00014',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):
        dwi_scan_labels = self.lut.get('DWI', [])

        failed = []
        exp_res = True
        columns = ['ID','xsiType','project',
                   'xnat:imageScanData/type',
                   'xnat:imageScanData/quality']
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=columns).data
        scans = {s['xnat:imagescandata/id']:s for s in scans}
        # filter out unsuitable scan_data items
        valid_scans = {
            str(scan_id): scan_data for scan_id,scan_data in scans.items()
            if __is_valid_scan__(self.xnat_instance, scan_data)
            and scan_data['xnat:imagescandata/type'].strip() in dwi_scan_labels}

        for e in valid_scans:
            res = HasBvecBval(self.lut, self.xnat_instance).run(experiment_id, e)
            if not res.has_passed:
                exp_res = False
                failed.append(e)
        return Results(exp_res, data={'failed':failed, 'dwi':valid_scans})

    def report(self):
        report = []
        if not self.results.has_passed:
            report.append('DWI scans without BVEC/BVAL: %s<br>'\
                %', '.join([str(e) for e in self.results.data['failed']]))

        report.append('Found DWI scans: %s'\
            %', '.join([str(e) for e in self.results.data['dwi']]))
        return report

class IsStudyDescriptionCorrect(ExperimentTest):
    '''Every scan should have its Study Description field matching the project's
    ID. This test passes only if all scans match the project's name.
    Fails otherwise.'''

    passing = 'BBRCDEV_E00014',
    failing = 'BBRCDEV_E00381',

    def aliases(self, project):
        uri = '/data/projects'
        options = {'columns': 'alias', 'format':'csv'}
        data = self.xnat_instance.get(uri, params=options).text
        from pyxnat.core.jsonutil import csv_to_json
        data = csv_to_json(unicode(data))

        # parse the results
        return [item['alias'] for item in data if item['alias'] and
                item['ID'] == project]

    def run(self, experiment_id):
        columns = ['xnat:imageSessionData/project',
                   'xnat:imageSessionData/session_type']
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=columns).data
        scans = {s['xnat:imagescandata/id']:s for s in scans}
        n = 0
        failed = []
        for k, v in scans.items():
            project = str(v['session_project'])
            session_type = v['session_type']
            if project != session_type:
                # attempt to check if StudyDescription matches a project ID alias
                #aliases = self.xnat_instance.select.project(project).aliases()
                aliases =  self.aliases(project)
                if not aliases or session_type not in aliases :
                    failed.append(session_type)

        res = len(failed) == 0
        return Results(res, data=list(set(failed)))

    def report(self):
        report = []
        if self.results.data:
            report.append('Incorrect ExamName found: %s' % ', '.join(self.results.data))
        return report

class HasCorrectSequences(ExperimentTest):
    '''Every protocol has a given list of sequences with specific number of
    frames per sequence. This check includes a series of controls (see
    `xnat-monitor`). Fails if a major sequence is missing or has a wrong number
    of frames. Passes if the major sequences are present with the right number
    of frames. Returns a summary of the performed controls.'''

    passing = 'BBRCDEV_E00380',
    failing = 'BBRCDEV_E00381',

    def run(self, experiment_id):

        def resolve_aliases(l, aliases, logs=[]):
            new_list = []
            transtab = {}
            for e in l:
                has_alias = False
                for k, v in aliases.items():
                    if e in v:
                        new_list.append(k)
                        logs.append('%s is found as %s<br>'%(k, e))
                        transtab[k] = e
                        has_alias = True
                if not has_alias:
                    new_list.append(e)
                    transtab[e] = e
            return new_list, transtab

        import json
        import bbrc
        import pandas as pd
        import os.path as op

        fp = op.join(op.dirname(bbrc.__file__), 'data', 'validation_rules.json')
        with open(fp, 'r') as f :
            rules = json.load(f)
        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID']
                                                      ).data[0]
        project_id = labels['project']

        # Ad-hoc exception added for DEVELOPMENT ENVIRONMENT test cases validation
        if project_id == 'testenv' and 'bscmaragall01' in self.xnat_instance._server :
            columns = ['ID','xnat:imagesessiondata/session_type']
            scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                                   columns = columns).data
            scans = {s['xnat:imagescandata/id']:s for s in scans}
            project_id = list(scans.items())[0][1]['session_type']
            project_id = project_id.replace('+','_PLUS')

        import logging as log
        log.info('*** %s'%project_id)
        # Sequences part
        seqdata = []
        d = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                           columns=['xnat:imageScanData/type',
                                                    'xnat:imageScanData/frames']
                                           ).data
        d = {s['xnat:imagescandata/id']:s for s in d}

        for scan_id, scan in d.items():
            row = [experiment_id]
            keys = ['xnat:imagescandata/id', 'xnat:imagescandata/type', 'xnat:imagescandata/frames']
            for k in keys:
                row.append(scan[k].rstrip(' '))  # Remove strange trailing spaces
                # for an example see ExamNames in:
                #  https://barcelonabrainimaging.org/data/experiments/BBRC02_E02410/scans/401/resources
            scan = self.xnat_instance.select.experiment(experiment_id).scan(scan_id)
            uri = scan._uri + '/resources'
            sc = {e['xnat_abstractresource_id']: e for e in self.xnat_instance._get_json(uri)}
            dcm_resources = {each['content']:each for each in sc.values() \
                if each['format'] == 'DICOM'}
            if len(dcm_resources) == 1 :
                row.append(list(dcm_resources.values())[0]['file_count'])
                seqdata.append(row)
            elif len(dcm_resources) == 2 and 'RAW' in dcm_resources.keys() :
                row.append(dcm_resources['RAW']['file_count'])
                seqdata.append(row)

        result = 0 # 0: OK   1: Warning   2:Error
        logs = []
        columns = ['xnatId', 'ID', 'type', 'frames', 'file_count']
        df = pd.DataFrame(seqdata, columns=columns)

        # Checks emptiness before starting anything
        df2 = df[df['xnatId'] == experiment_id][['ID', 'type', 'frames', 'file_count']]
        session_seqlist = df2['type'].tolist() # List of sequences of the session

        if df2.empty:
            logs.append('%s scan data not found'%experiment_id)
            return Results(False, data=['Scan data not found'])

        # Dropping mock sequences: could probably use utils.__is_valid_scan__
        for index, row in df2.iterrows():
            if row['ID'].startswith('0-') or 'OT' in row['ID']:
                logs.append('Ignoring sequence %s<br>'%row['ID'])
                session_seqlist.remove(row['type'])
                df2.drop(index, inplace=True)

        # If the project does not have predefined rules, set default (empty) rules
        pr = rules.get(project_id, {'obligatory': {},
                                    'aliases': {},
                                    'warning_if_missing': {},
                                    'silently_identified': {}})
        if project_id not in rules:
            msg = 'No found validation results for %s.'%project_id
            log.error(msg)
            return Results(None, data=[msg])

        # Resolving aliases, transtab is a translation table
        session_seqlist, transtab = resolve_aliases(session_seqlist,
                                                    pr['aliases'],
                                                    logs)


        # Checking obligatory sequences
        for k, v in pr['obligatory'].items():

            key = 'frames' if k in transtab and not 'CHESS' in transtab[k] \
                else 'file_count'

            if session_seqlist.count(k) == 1:
                n_frames = df2[df2['type'] == transtab[k]][key].iloc[0]
                if n_frames != str(v):
                    msg = '*** %s is unique but has wrong file_count '\
                        '(%s instead of %s) ***<br>'%(k, n_frames, v)
                    logs.append(msg)
                    result = 2
            if session_seqlist.count(k) > 1:
                occ = df2[df2['type']==transtab[k]]['ID'].tolist()
                logs.append('%s multiple occurrences (%s)<br>'%(k, occ))
                result = max(result, 1)

        logs.append('<br> ===== Missing ========<br>')
        for k, v in pr['obligatory'].items():
            if not k in session_seqlist:
                logs.append('*** %s is obligatory and missing ***<br>'%k)
                result = max(result, 2)
        for k in pr['warning_if_missing']:
            if not k in session_seqlist:
                logs.append('%s missing<br>'%k)
                result = max(result, 1)

        logs.append('<br> ========= Not identified ==========<br>')

        seq = list(pr['obligatory'].keys())
        seq.extend(pr['warning_if_missing'])
        seq.extend(pr['silently_identified'])
        for k, v in pr['aliases'].items():
            seq.extend(v)
        for each in set(session_seqlist).difference(seq):
            logs.append('%s not identified<br>'%each)

        logs.append('<br> ========= Silently identified ==========<br>')
        for each in session_seqlist:
            if each in pr['silently_identified']:
                logs.append('%s silently identified<br>'%each)

        res = result != 2
        return Results(res, data = logs)

class HasCorrectSequenceAttributes(ExperimentTest):
    '''
    Every relevant scanning protocol has a set of DICOM metadata attributes
    describing -among other things- the acquisition protocol parameters used and
    the imaging data itself.
    This check validates a subset of DICOM attributes against predefined
    accepted values for each relevant scanning sequence in the dataset.
    Fails if any relevant sequence has an unexpected value for a DICOM metadata
    attributes. Passes if all the sequence-specific DICOM metadata attributes
    are present and with tolerable values.
    '''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):

        import json
        import bbrc
        import os.path as op
        import logging as log
        import numpy as np

        alfa_protocols = ['B0_ALFA1', 'T1_ALFA1', 'T2_ALFA1',
                          'FLAIR_ALFA1','DWI_ALFA1', 'RS_ALFA1_SENSE']
        protocol_attributes = {}
        for seq in alfa_protocols :
            fp = op.join(op.dirname(bbrc.__file__), 'data',
                         'protocol_validation', '%s.json'%seq)
            with open(fp, 'r') as f :
                protocol_attributes[seq] = json.load(f)

        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=['ID',
                                                        'xsiType',
                                                        'xnat:imageSessionData/project',
                                                        'xnat:imageScanData/type',
                                                        'xnat:imageScanData/quality']
                                               ).data
        scans = {s['xnat:imagescandata/id']:s for s in scans}


        project_id = str(list(scans.items())[0][1]['session_project'])

        matched_scans = {str(ID): str(scans[ID]['xnat:imagescandata/type']).strip().replace(" ", "_") for ID in scans
                         if str(scans[ID]['xnat:imagescandata/type']).strip().replace(" ", "_") in protocol_attributes.keys()
                         and not str(ID).startswith('0')
                         and scans[ID]['xnat:imagescandata/quality'] == 'usable'
                         and self.xnat_instance.select.experiment(experiment_id).scan(ID).datatype() == 'xnat:mrScanData'
                         }

        if not matched_scans:
            msg = 'Session %s (%s) has no scans matching any of the relevant '\
                'scanning protocols'%(experiment_id,project_id)
            log.warning(msg)
            return Results(False, data='Unknown scanning protocols')

        validation_data = {}
        for scan_id in matched_scans:
            uri = '/REST/services/dicomdump'
            options = {
                'format': 'csv',
                'src': '/archive/projects/%s/experiments/%s/scans/%s' %(project_id,experiment_id,scan_id),
                'field': ['00189087', '00200105', '00081090', '00080008', '0008103E', '00080070',
                          '00181020', '00181000', '00180015', '00180023', '00180050', '00180080',
                          '00180081', '00180083', '00180087', '00180088', '00180089', '00180095',
                          '00181310', '00181312', '00181314', '00185100', '00189073', '00280010',
                          '00280011', '00280030']
            }

            #dicom_dump = self.xnat_instance._get_json(uri, body=options)
            from pyxnat.core.jsonutil import csv_to_json
            dicomdump = csv_to_json(unicode(self.xnat_instance.get(uri, params=options).text))

            dicom_attributes = {
                str(item['desc']).replace(" ", "").replace("&rsquo;s", "s") : str(item['value'])
                for item in dicomdump
            }

            scan_validation_results = {}
            for tag, value in protocol_attributes[matched_scans[scan_id]].items():
                result = False
                if tag in dicom_attributes.keys():

                    if isinstance(value, string_types):
                        if tag == 'SeriesDescription':
                            # exception: In some cases SeriesDescription value should be preprocessed to match the protocol name
                            result = bool(value == dicom_attributes[tag].strip().replace(" ", "_"))
                        else:
                            result = bool(value == dicom_attributes[tag])
                    elif isinstance(value, int):
                        # exception: PixelBandwith diverges greatly at T1W,RS,... Tolerance factor of +/- 1%
                        if tag == 'PixelBandwidth':
                            import math
                            tolerance = int(math.ceil(0.01 * value))
                            result = bool(np.isclose(int(dicom_attributes[tag]), value, atol=tolerance))
                        else:
                            result = bool(int(dicom_attributes[tag]) == value)
                    elif isinstance(value, float):
                        # exception: RepetitionTime diverges frequently. Tolerance factor of +/- 1 (absolute)
                        if tag == 'RepetitionTime':
                            result = bool(np.isclose(float(dicom_attributes[tag]), value, atol=1))
                        # exception: AcquisitionDuration diverges (particularly in FLAIR!). Tolerance factor of +/- 5 (absolute)
                        elif tag == 'AcquisitionDuration':
                            result = bool(np.isclose(float(dicom_attributes[tag]), value, atol=5))
                        else:
                            # note: tolerance added for the float typed values of +/- 0.05 (absolute)
                            result = bool(np.isclose(float(dicom_attributes[tag]), value, atol=0.05))
                    elif isinstance(value, list):
                        # exception: Diffusion b-value for DWI scans can have several values (depending on the current slice/file)
                        if tag == 'Diffusionb-value':
                            result = round(float(dicom_attributes[tag]), 3) in value
                        # exception: PixelSpacing values diverge slightly (+/- 0.001)
                        elif tag == 'PixelSpacing':
                            result = all(np.isclose(np.asarray(dicom_attributes[tag].split('\\')).astype(np.float),
                                                    np.asarray(value).astype(np.float),
                                                    atol=0.001))
                        # exception: SoftwareVersions can either be 5.1.9 or 5.4.0
                        elif tag == 'SoftwareVersion(s)':
                            result = bool(dicom_attributes[tag].split('\\') in value)
                        else:
                            result = bool(dicom_attributes[tag].split('\\') == value)
                else:
                    log.error('Scan %s (%s) has no %s DICOM tag'%(scan_id, experiment_id, tag))

                scan_validation_results[tag] = result

            # Populate useful resulting data if Test failed
            if not all(scan_validation_results.values()):
                for k,v in scan_validation_results.items() :
                    if not v :
                        if k in dicom_attributes.keys():
                            validation_data[scan_id] = (k, dicom_attributes[k])
                        else :
                            validation_data[scan_id] = (k, "DICOM tag not found")

        validation_result = bool(len(validation_data) == 0)
        return Results(validation_result, data = validation_data)

    def report(self):
        report = []
        if not self.results.has_passed :
            if isinstance(self.results.data,dict) :
                report.append('Relevant scans with invalid DICOM attributes:<br>')
                report.append('<br>'.join(['%s: %s (%s)'%(k,v[0],v[1]) for k,v in self.results.data.items()]))
            else :
                report.append(self.results.data)

        return report

class IsFreeSurferRunnable(ExperimentTest):
    '''This check validates that the given MRSession fulfills the requirements
    for running FreeSurfer application.
    Fails if no MRSession scans are suited for running FreeSurfer (see
    result/report data), passes otherwise.'''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00483',

    def run(self, experiment_id):
        res = HasUsableT1(self.lut, self.xnat_instance).run(experiment_id)
        if not res.has_passed:
            return Results(False, data=['%s Not runnable.' % res.data[0]])
        return Results(True, data=[])

class HasUsableT1(ExperimentTest):
    '''This test determines if session has a usable T1-weighted (`T1`) scan
    suited for further processing. This test passes either if there is
    one unique and valid sequence labelled as T1 or if, in case of multiple
    matches, only one of them is labelled as `usable`. Fails otherwise.'''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00483',

    def run(self, experiment_id):
        t1w_scan_labels = self.lut.get('T1', [])

        columns = ['xnat:mrScanData/type',
                   'xnat:mrScanData/quality',
                   'xnat:mrScanData/frames']

        scans = self.xnat_instance.array.mrscans(experiment_id=experiment_id,
                                                 columns=columns).data
        scans = {s['xnat:mrscandata/id']:s for s in scans}

        # filter out unsuitable scan_data items
        valid_t1w_scans = {
            str(scan_id) : scan_data for scan_id,scan_data in scans.items()
            if __is_valid_scan__(self.xnat_instance, scan_data)
            and scan_data['xnat:mrscandata/type'].strip() in t1w_scan_labels}

        if not valid_t1w_scans :
            return Results(False, data=['No valid T1 scans found.'])

        has_preferredT1 = HasPreferredT1(self.lut, self.xnat_instance).run(experiment_id)
        if not has_preferredT1.has_passed:
            msg = 'Multiple T1 scans but unable to determine a preferred one.'
            return Results(False, data=[msg])

        scan_id = list(has_preferredT1.data)[0]

        # built-in checks
        required = [HasNifti, HasUncompressedPixelData, IsClassicDICOM]

        for each in required:
            c = each(self.lut, self.xnat_instance).run(experiment_id, scan_id)
            if not c.has_passed:
                msg = 'Test %s failed.'%each.__name__
                return Results(False, data=[msg])

        return Results(True, data=[scan_id])

    def report(self):
        if self.results.has_passed:
            report = ['Usable T1: %s' %list(self.results.data)[0]]
        else:
            report = [list(self.results.data)[0]]
        return report

class HasPreferredT1(ExperimentTest):
    '''Sessions may have multiple versions of T1 images (captured by
    HasDuplicatedSequence). In those cases, and in order to identify which one
    may have the best quality and be selected for further processing, it is
    possible to rely on the possibly associated reconstructions along other axes
    e.g. AXIAL and CORONAL). It is assumed that reconstructed versions are
    generated for the preferred version of the T1 scan only.
    This test passes either if there is one unique and valid T1 sequence or if,
    in case of multiple matches, only one of them has suitable associated
    reconstructions. Note that in those cases, the Test will proactively label
    all scans without reconstructions as `questionable`, excluding them for any
    processing stage (corrective measure).'''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00483',

    def valid_T1w_scans(self, experiment_id):
        ''' Returns a dictionary of 'valid' T1 scans for a given
        experiment_id. '''
        t1w_scan_labels = self.lut.get('T1', [])

        options = ['xnat:imagescandata/quality','xsiType',
                    'xnat:imagescandata/frames', 'xnat:imagescandata/type']
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=options).data
        valid_t1w_scans = {
            str(scan['xnat:imagescandata/id']) : scan for scan in scans
            if __is_valid_scan__(self.xnat_instance, scan)
            and scan['xnat:imagescandata/type'].strip() in t1w_scan_labels
        }
        return valid_t1w_scans

    def reconstructed_scans(self, experiment_id, scan_id):
        ''' Given an experiment_id and a scan_id, returns a set of existing
        matching scan IDs. '''

        options = ['xnat:imagescandata/quality','xsiType',
                    'xnat:imagescandata/frames', 'xnat:imagescandata/type']
        scans = self.xnat_instance.array.scans(experiment_id=experiment_id,
                                               columns=options).data
        series = [scan for scan in scans
                  if len(scan['xnat:imagescandata/id']) == len(scan_id) \
                  and scan['xnat:imagescandata/id'][:-1] == scan_id[:-1]]
        return series

    def has_reconstructed_scans(self, scans):
        ''' Given a set of scan IDs, returns a boolean if these refer to a
        collection of reconstructed scans '''

        seq = {}
        for each in ['alfa1', 'coronal', 'axial']:
            seq[each] = []
            for v in scans:
                if each in v['xnat:imagescandata/type'].lower():
                    seq[each].append(v['ID'])
        return len(seq['alfa1']) * len(seq['coronal']) * len(seq['axial']) == 1

    def set_scan_quality_label(self, experiment_id, scan_id, label):
        ''' Set the quality label for a given experiment/scan. '''

        import logging as log
        assert(label in ['usable','questionable','unusable'])
        uri = 'data/experiments/%s/scans/%s'%(experiment_id, scan_id)

        data = {'xsiType': 'xnat:mrScanData',
                'xnat:mrscandata/quality': label}
        r = self.xnat_instance.put(uri, data=data)
        log.warning('Setting scan %s (%s) quality to `%s`.'%(scan_id,experiment_id,label))
        return r

    def __is_reconstructed__(self, experiment_id):
        valid_t1w_scans = self.valid_T1w_scans(experiment_id)
        is_reconstructed = {}
        for scan_id in valid_t1w_scans.keys():
            reconstructed = self.reconstructed_scans(experiment_id, scan_id)
            is_reconstructed[scan_id] = self.has_reconstructed_scans(reconstructed)

        return is_reconstructed

    def preferred_T1(self, experiment_id):
        ''' Returns the scan_id of the preferred T1 given an experiment_id. '''

        valid_t1w_scans = self.valid_T1w_scans(experiment_id)

        if not valid_t1w_scans :
            return None
        elif len(valid_t1w_scans.keys()) == 1 :
            return list(valid_t1w_scans.keys())[0]

        is_reconstructed = self.__is_reconstructed__(experiment_id)
        has_unique = list(is_reconstructed.values()).count(True) == 1
        if has_unique:
            return list(is_reconstructed.keys())[0]
        else:
            return None

    def run(self, experiment_id):
        valid_t1w_scans = self.valid_T1w_scans(experiment_id)

        if not valid_t1w_scans :
            return Results(False, data=['No valid T1 scans found.'])
        elif len(valid_t1w_scans.keys()) == 1 :
            return Results(True, data=list(valid_t1w_scans.keys()))

        is_reconstructed = self.__is_reconstructed__(experiment_id)
        has_unique = list(is_reconstructed.values()).count(True) == 1

        reconstructed = [e for e, v in is_reconstructed.items()\
                         if v is True]
        not_reconstructed = [e for e, v in is_reconstructed.items()\
                         if v is False]

        preferred = self.preferred_T1(experiment_id)

        if not preferred is None:
            # apply corrective measure!
            for scan in not_reconstructed:
                self.set_scan_quality_label(experiment_id,
                                       scan, 'questionable')

        return Results(has_unique, data=reconstructed)

    def report(self):
        if self.results.has_passed:
            report = ['Preferred T1: %s'%list(self.results.data)[0]]
        else:
            if not self.results.data :
                report = ['No T1 scans found with reconstructed versions']
            else :
                reconstructed = list(self.results.data)[0]
                if not isinstance(reconstructed, str):
                    report = ['Following T1 scans were found with reconstructed '\
                        'versions: %s'%', '.join(reconstructed)]
                else:
                    report = [list(self.results.data)[0]]
        return report

class IsPhilipsVersion519(ExperimentTest):
    '''
    The scanner software version used for generating an MRI dataset is
    registered in the DICOM metaheader as `SoftwareVersion(s)`.
    This test passes if an MRI Session was acquired using version 5.1.9 of the
    manufacturers software. Fails otherwise.
    If no SoftwareVersion(s) attribute is found in the DICOM metaheader, the
    test is skipped.
    '''

    passing = 'BBRCDEV_E00375',
    failing = 'BBRCDEV_E00401',

    def run(self, experiment_id):

        MRI_SOFTWARE_VERSION = ['5.1.9', '5.1.9.1']

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID']
                                                      ).data[0]
        project_id = str(labels['project'])

        uri = '/REST/services/dicomdump'
        options = {
            'format': 'csv',
            'src': '/archive/projects/%s/experiments/%s' %(project_id,experiment_id),
            'field': '00181020'
        }
        from pyxnat.core.jsonutil import csv_to_json
        tag = csv_to_json(unicode(self.xnat_instance.get(uri, params=options).text))
        if not tag :
            return Results(None, ['Software Versions (0018,1020) tag is not present'])
        tag_value = str(tag[0]['value']).split('\\')

        result = False
        data = ['Unexpected version: %s' % tag_value]
        if len(tag_value) == 2 and tag_value == MRI_SOFTWARE_VERSION :
            result = True
            data = []
        elif len(tag_value) == 1 and tag_value[0] in MRI_SOFTWARE_VERSION :
            result = True
            data = []
        return Results(result, data)

class IsPhilipsVersion540(ExperimentTest):
    '''
    The scanner software version used for generating an MRI dataset is
    registered in the DICOM metaheader as `SoftwareVersion(s)`.
    This test passes if an MRI Session was acquired using version 5.4.0 of the
    manufacturers software. Fails otherwise.
    If no SoftwareVersion(s) attribute is found in the DICOM metaheader, the
    test is skipped.
    '''

    passing = 'BBRCDEV_E00401',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):

        MRI_SOFTWARE_VERSION = ['5.4.0', '5.4.0.0']

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID']
                                                      ).data[0]
        project_id = str(labels['project'])

        uri = '/REST/services/dicomdump'
        options = {
            'format': 'csv',
            'src': '/archive/projects/%s/experiments/%s' %(project_id,experiment_id),
            'field': '00181020'
        }
        from pyxnat.core.jsonutil import csv_to_json
        tag = csv_to_json(unicode(self.xnat_instance.get(uri, params=options).text))
        if not tag :
            msg = 'Software Versions (0018,1020) tag is not present'
            return Results(None, [msg])
        tag_value = str(tag[0]['value']).split('\\')

        result = False
        data = ['Unexpected version: %s' % tag_value]
        if len(tag_value) == 2 and tag_value == MRI_SOFTWARE_VERSION:
            result = True
            data = []
        elif len(tag_value) == 1 and tag_value[0] in MRI_SOFTWARE_VERSION:
            result = True
            data = []
        return Results(result, data)

class IsAccessionNumberUnique(ExperimentTest):
    '''
    The AccessionNumber (AN) is a supposedly unique code that contains project,
    session/visit and study date information.
    This test passes if an MRI Session has its AN consistently unique across the
     current XNAT instance. Fails otherwise. If the MRI Session project is in
     the excluded projects list, the test is skipped.
    '''

    passing = 'BBRCDEV_E00403',
    failing = 'BBRCDEV_E00405',

    def get_all_projects(self, connection):
        '''Query XNAT REST interface for full project list'''
        '''Returns a dict of project IDs and metainformation'''

        # compose the URL for the REST call
        uri = '/data/projects?accessible=true'

        # do the HTTP query
        projects = connection._get_json(uri)

        # parse the results
        projectDict = {}
        for project in projects:
            projectDict[project['id']] = project

        return projectDict


    def run(self, experiment_id):
        # Exclude testing/external projects which are not relevant
        excluded_projects = ['UCLM', 'HUGM', 'UPF_IR', 'PHILIPS', 'TEST_MRI',
                             'VOLUNTARIOS', 'jh_sandbox', 'GE-AIBL', 'BLSA']
        all_projects = self.get_all_projects(self.xnat_instance).keys()
        #all_projects = list(self.xnat_instance.select.projects())
        projects = [e for e in all_projects if e not in excluded_projects]

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID']
                                                      ).data[0]

        project_id = str(labels['project'])
        session_label = str(labels['label'])

        # XNAT does not allow having distinct experiments with same label in a
        # contiguous Project container exclude current project from the list of
        # projects to check for
        if project_id not in projects :
            msg = 'Project excluded for AccessionNumber consistency checks.'
            return Results(None, data=[msg])
        else:
            projects.remove(project_id)

        matchings = {}
        for project in projects:
            seslist = self.xnat_instance.array.experiments(project_id=project,
                                                           columns=['ID',
                                                                    'label']
                                                           ).data
            pmatches = [e['ID'] for e in seslist if str(session_label) == e['label']]
            if pmatches:
                matchings[project] = pmatches[0]

        data = []
        if matchings :
            msg = 'AccessionNumber (%s) is not unique, matchings: %s'\
                %(session_label, matchings)
            data = [msg]

        return Results(bool(len(data)==0), data)

class HasValidAccessionNumber(ExperimentTest):
    '''
    This test passes if an MRI Session AccessionNumber (AN) can be parsed and
    its project, session/visit and date information is valid and consistent.
    Fails otherwise. If the MRI Session project is in the excluded projects
    list, the test is skipped.
    '''

    passing = 'BBRCDEV_E00403',
    failing = 'BBRCDEV_E00404',

    def parse_AccessionNumber(self, an_code):

        if len(an_code) == 15:
            p_code = an_code[0:2]
            v_code = an_code[2:4]
            subject = an_code[4:6] + an_code[12:15]
            date = an_code[6:12]
        elif len(an_code) == 16:
            p_code = an_code[0:2]
            v_code = an_code[2:5]
            subject = an_code[5:7] + an_code[13:16]
            date = an_code[7:13]
        else:
            return None

        return p_code, v_code, subject, date


    def run(self, experiment_id):

        import json
        import bbrc
        import os.path as op
        from datetime import datetime as dt

        # Exclude testing/external projects which are not relevant
        excluded_projects = ['UCLM', 'HUGM', 'UPF_IR', 'PHILIPS', 'TEST_MRI',
                             'VOLUNTARIOS', 'jh_sandbox', 'GE-AIBL', 'BLSA']

        fp = op.join(op.dirname(bbrc.__file__), 'data', 'an_codes.json')
        with open(fp, 'r') as f:
            codes = json.load(f)

        labels = self.xnat_instance.array.experiments(experiment_id=experiment_id,
                                                      columns=['ID',
                                                               'label',
                                                               'project',
                                                               'subject_ID',
                                                               'subject_label']
                                                      ).data[0]

        session_id = str(labels['label'])
        subject_label = str(labels['subject_label'])
        project_id = str(labels['project'])
        # Handle project name exception for ALFA_PLUS2 (which is actually part
        # of ALFA_PLUS study)
        if project_id == 'ALFA_PLUS2':
            project_id = project_id[:-1]

        parsed = self.parse_AccessionNumber(session_id)
        if not parsed:
            msg = 'AccessionNumber %s cannot be parsed'%session_id
            return Results(False, data=[msg])
        pr_code, vi_code, subject, date = parsed

        # A) check if project & visit prefix codes are CORRECT
        if pr_code not in codes.keys():
            msg = 'Invalid AccessionNumber prefix (project code \'%s\')'%pr_code
            return Results(False, data=[msg])
        else:
            if codes[pr_code]['project'] != project_id:
                msg = 'Project code (%s) not matching current project' \
                    %codes[pr_code]['project']
                return Results(False, data=[msg])
            else:
                if vi_code not in codes[pr_code]['visit_codes'].keys():
                    msg = 'Invalid AccessionNumber prefix (visit code \'%s\')'%vi_code
                    return Results(False, data=[msg])

        # B) check if date code is CORRECT
        #options = {'ID': experiment_id, 'columns': 'ID,label,date'}
        session_data = self.xnat_instance.array.experiments(project_id=str(labels['project']),
                                                            columns=['ID',
                                                                     'label',
                                                                     'date']
                                                            ).data
        session_data = {e['ID'] : e for e in session_data}
        session_date = dt.strptime(session_data[experiment_id]['date'], '%Y-%m-%d')
        try:
            an_date = dt.strptime(date, '%d%m%y')
        except ValueError:
            return Results(False,data=['Invalid AccessionNumber prefix (date \'%s\')'%date])

        if an_date != session_date:
            return Results(False, data=['Date (%s) not matching current acquisition date'%dt.date(an_date)])

        # C) check if subject is CORRECT
        if subject != subject_label:
            return Results(False, data=['Subject (%s) not matching current subject for %s'%(subject, session_id)])

        return Results(True, data=[])

class IsDtifitRunnable(ExperimentTest):
    '''This check validates that the given MRSession fulfills the requirements
    for running FSL dtifit application. Fails if no MRSession scans are suited
    for running dtifit (see result/report data), passes otherwise.'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):
        res_dwi = HasUsableDWI(self.lut, self.xnat_instance).run(experiment_id)
        if not res_dwi.has_passed:
            return Results(False, data=['%s Not runnable.' %res_dwi.data[0]])

        res_rdwi = HasUsableReversedDWI(self.lut, self.xnat_instance).run(experiment_id)
        if not res_rdwi.has_passed:
            return Results(False, data=['%s Not runnable.' % res_rdwi.data[0]])

        return Results(True, data=[])

class HasUsableDWI(ExperimentTest):
    '''This test determines if session has a usable Diffusion-weighted (`DWI`)
    scan suited for further processing. This test passes either if there is
    one unique and valid DWI sequence or if, in case of multiple matches,
    only one of them is labelled as `usable`. Fails otherwise.'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):
        dwi_scan_labels = self.lut.get('DWI', [])

        columns = ['xsiType',
                   'xnat:mrScanData/type',
                   'xnat:mrScanData/quality',
                   'xnat:mrScanData/frames']

        scans = self.xnat_instance.array.mrscans(experiment_id=experiment_id,
                                               columns=columns).data
        scans = {s['xnat:mrscandata/id']:s for s in scans}

        # filter out unsuitable scan_data items
        valid_scans = {
            str(scan_id) : scan_data for scan_id,scan_data in scans.items()
            if __is_valid_scan__(self.xnat_instance, scan_data)
            and scan_data['xnat:mrscandata/type'].strip() in dwi_scan_labels}

        if not valid_scans :
            return Results(False, data=['No valid DWI scans found.'])
        elif len(valid_scans) > 1 :
            return Results(False, data=['Multiple DWI scans.'])

        scan_id = list(valid_scans.keys())[0]

        # built-in checks
        required = [HasBvecBval, HasNifti, IsClassicDICOM,
                    HasPhilipsPrivateTags, HasUncompressedPixelData]

        for each in required:
            c = each(self.lut, self.xnat_instance).run(experiment_id, scan_id)
            if not c.has_passed:
                msg = 'Test %s failed.' %each.__name__
                return Results(False, data=[msg])

        return Results(True, data=[scan_id])

    def report(self):
        if self.results.has_passed:
            report = ['Usable DWI: %s' %list(self.results.data)[0]]
        else:
            report = [list(self.results.data)[0]]
        return report

class HasUsableT2(ExperimentTest):
    '''Test determines if session has a usable T2-weighted (`T2`) scan
    suited for further processing. This test passes either if there is
    one unique and valid T2 sequence or if, in case of multiple matches,
    only one of them is labelled as `usable`. Fails otherwise.'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):
        t2w_scan_labels = self.lut.get('T2', [])

        columns = ['xnat:mrScanData/type',
                   'xnat:mrScanData/quality',
                   'xnat:mrScanData/frames']

        data = self.xnat_instance.array.mrscans(experiment_id=experiment_id,
                                                 columns=columns).data
        scans = {s['xnat:mrscandata/id']:s for s in data}

        # filter out unsuitable scan_data items
        valid_scans = {
            str(scan_id) : scan_data for scan_id,scan_data in scans.items()
            if __is_valid_scan__(self.xnat_instance, scan_data)
            and scan_data['xnat:mrscandata/type'].strip() in t2w_scan_labels}

        if not valid_scans :
            return Results(False, data=['No valid T2 scans found.'])
        elif len(valid_scans) > 1 :
            return Results(False, data=['Multiple T2 scans.'])

        scan_id = list(valid_scans.keys())[0]

        # built-in checks
        required = [HasNifti, IsClassicDICOM, HasUncompressedPixelData]

        for each in required:
            c = each(self.lut, self.xnat_instance).run(experiment_id, scan_id)
            if not c.has_passed:
                msg = 'Test %s failed.' %each.__name__
                return Results(False, data=[msg])

        return Results(True, data=[scan_id])

    def report(self):
        if self.results.has_passed:
            report = ['Usable T2: %s' %list(self.results.data)[0]]
        else:
            report = [list(self.results.data)[0]]
        return report

class IsT2T1CoregistrationRunnable(ExperimentTest):
    '''This test validates that the given MRSession fulfills the requirements
    to run a multimodal pipeline for the coregistration of T2 scan image into T1
    image space. Fails if no MRSession scans are suited for running
    `T2T1Coregistraton` pipeline, passes otherwise.'''

    passing = 'BBRCDEV_E01613',
    failing = 'BBRCDEV_E00385',

    def run(self, experiment_id):

        res_t1 = HasUsableT1(self.lut, self.xnat_instance).run(experiment_id)
        if not res_t1.has_passed:
            return Results(False, data=['%s Not runnable.' %res_t1.data[0]])

        res_t2 = HasUsableT2(self.lut, self.xnat_instance).run(experiment_id)
        if not res_t2.has_passed:
            return Results(False, data=['%s Not runnable.' %res_t2.data[0]])

        return Results(True, data=[])

class HasUsableIR(ExperimentTest):
    '''Test determines if session has a usable Inversion Recovery (`IR`) scan
    suited for further processing. This test passes either if there is
    one unique and valid IR sequence or if, in case of multiple matches,
    only one of them is labelled as `usable`. Fails otherwise.'''

    passing = 'BBRCDEV_E02443',
    failing = 'BBRCDEV_E00281',

    def run(self, experiment_id):
        ir_scan_labels = self.lut.get('IR', [])

        columns = ['xnat:mrScanData/type',
                   'xnat:mrScanData/quality',
                   'xnat:mrScanData/frames']

        data = self.xnat_instance.array.mrscans(experiment_id=experiment_id,
                                                 columns=columns).data
        scans = {s['xnat:mrscandata/id']:s for s in data}

        # filter out unsuitable scan_data items
        valid_scans = {
            str(scan_id) : scan_data for scan_id,scan_data in scans.items()
            if __is_valid_scan__(self.xnat_instance, scan_data)
            and scan_data['xnat:mrscandata/type'].strip() in ir_scan_labels}

        if not valid_scans :
            return Results(False, data=['No valid IR scans found.'])
        elif len(valid_scans) > 1 :
            return Results(False, data=['Multiple IR scans.'])

        scan_id = list(valid_scans.keys())[0]

        # built-in checks
        required = [HasNifti, IsClassicDICOM, HasUncompressedPixelData]

        for each in required:
            c = each(self.lut, self.xnat_instance).run(experiment_id, scan_id)
            if not c.has_passed:
                msg = 'Test %s failed.' %each.__name__
                return Results(False, data=[msg])

        return Results(True, data=[scan_id])

    def report(self):
        if self.results.has_passed:
            report = ['Usable IR: %s' %list(self.results.data)[0]]
        else:
            report = [list(self.results.data)[0]]
        return report

class IsASHSRunnable(ExperimentTest):
    '''This test validates that the given MRSession fulfills the requirements
    to run `ASHS`, a multimodal pipeline for the segmentation of hippocampal
    subfields that uses a T1w and a Inversion Recovery (IR) set of scan images.
    Fails if no MRSession scans are suited for running `ASHS` pipeline, passes
    otherwise.'''

    passing = 'BBRCDEV_E02443',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):

        res_t1 = HasUsableT1(self.lut, self.xnat_instance).run(experiment_id)
        if not res_t1.has_passed:
            return Results(False, data=['%s Not runnable.' %res_t1.data[0]])

        res_ir = HasUsableIR(self.lut, self.xnat_instance).run(experiment_id)
        if not res_ir.has_passed:
            return Results(False, data=['%s Not runnable.' %res_ir.data[0]])

        return Results(True, data=[])

class HasUsableReversedDWI(ExperimentTest):
    '''This test determines if session has a usable reversed phase-encoding
    Diffusion-weighted (`rDWI`) scan suited for further processing. This test
    passes either if there is one unique and valid rDWI sequence or if, in case
    of multiple matches, only one of them is labelled as `usable`. Fails otherwise.'''

    passing = 'BBRCDEV_E00272',
    failing = 'BBRCDEV_E00007',

    def run(self, experiment_id):
        dwi_scan_labels = self.lut.get('rDWI', [])

        columns = ['xsiType',
                   'xnat:mrScanData/type',
                   'xnat:mrScanData/quality',
                   'xnat:mrScanData/frames']

        scans = self.xnat_instance.array.mrscans(experiment_id=experiment_id,
                                               columns=columns).data
        scans = {s['xnat:mrscandata/id']:s for s in scans}

        # filter out unsuitable scan_data items
        valid_scans = {
            str(scan_id) : scan_data for scan_id,scan_data in scans.items()
            if __is_valid_scan__(self.xnat_instance, scan_data)
            and scan_data['xnat:mrscandata/type'].strip() in dwi_scan_labels}

        if not valid_scans :
            return Results(False, data=['No valid rDWI scans found.'])
        elif len(valid_scans) > 1 :
            return Results(False, data=['Multiple rDWI scans.'])

        scan_id = list(valid_scans.keys())[0]

        # built-in checks
        required = [HasNifti, IsClassicDICOM, HasUncompressedPixelData]

        for each in required:
            c = each(self.lut, self.xnat_instance).run(experiment_id, scan_id)
            if not c.has_passed:
                msg = 'Test %s failed.' %each.__name__
                return Results(False, data=[msg])

        return Results(True, data=[scan_id])

    def report(self):
        if self.results.has_passed:
            report = ['Usable rDWI: %s' %list(self.results.data)[0]]
        else:
            report = [list(self.results.data)[0]]
        return report