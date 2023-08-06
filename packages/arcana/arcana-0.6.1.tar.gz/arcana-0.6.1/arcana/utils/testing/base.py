from __future__ import print_function
from past.builtins import basestring
import os.path as op
import os
from arcana.utils import makedirs
import subprocess as sp
import shutil
from unittest import TestCase
import errno
import sys
import json
from arcana.utils import JSON_ENCODING
import filecmp
from copy import deepcopy
import logging
import arcana
from arcana.data import Fileset, FilesetSlice
from arcana.utils import classproperty
from arcana.repository import Dataset, LocalFileSystemRepo
from arcana.processor import SingleProc
from arcana.environment import StaticEnv
from arcana.exceptions import ArcanaError
from arcana.exceptions import ArcanaUsageError

logger = logging.getLogger('arcana')
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

wf_logger = logging.getLogger('nipype.workflow')
wf_logger.setLevel(logging.WARNING)
intf_logger = logging.getLogger('nipype.interface')
intf_logger.setLevel(logging.WARNING)

logging.getLogger("urllib3").setLevel(logging.WARNING)


class BaseTestCase(TestCase):

    SUBJECT = 'SUBJECT'
    VISIT = 'VISIT'
    SESSION = (SUBJECT, VISIT)
    REF_FORMATS = None
    XNAT_TEST_PROJECT = None
    STUDY_NAME = None

    # Whether to copy reference filesets from reference directory
    INPUTS_FROM_REF_DIR = False

    # The path to the test directory, which should sit along side the
    # the package directory. Note this will not work when Arcana
    # is installed by a package manager.
    BASE_TEST_DIR = op.abspath(op.join(
        op.dirname(arcana.__file__), '..', 'test'))

    @classproperty
    @classmethod
    def test_data_dir(cls):
        try:
            return cls._test_data_dir
        except AttributeError:
            try:
                cls._test_data_dir = os.environ['ARCANA_TEST_DATA']
                makedirs(cls._test_data_dir, exist_ok=True)
            except KeyError:
                cls._test_data_dir = op.join(cls.BASE_TEST_DIR, 'data')
            return cls._test_data_dir

    @classproperty
    @classmethod
    def unittest_root(cls):
        return op.join(cls.BASE_TEST_DIR, 'unittests')

    @classproperty
    @classmethod
    def dataset_path(cls):
        return op.join(cls.test_data_dir, 'dataset')

    @classproperty
    @classmethod
    def work_path(cls):
        return op.join(cls.test_data_dir, 'work')

    @classproperty
    @classmethod
    def cache_path(cls):
        return op.join(cls.test_data_dir, 'cache')

    @classproperty
    @classmethod
    def ref_path(cls):
        return op.join(cls.BASE_TEST_DIR, 'data', 'reference')

    def setUp(self):
        self.reset_dirs()
        if self.INPUTS_FROM_REF_DIR:
            filesets = {}
            # Unzip reference directory if required
            if not os.path.exists(self.ref_dir) and os.path.exists(
                    self.ref_dir + '.tar.gz'):
                sp.check_call(
                    'tar xzf {}.tar.gz'.format(self.ref_dir),
                    shell=True, cwd=os.path.dirname(self.ref_dir))
            for fname in os.listdir(self.ref_dir):
                if fname.startswith('.'):
                    continue
                fileset = Fileset.from_path(op.join(self.ref_dir,
                                                    fname))
                fileset.format = fileset.detect_format(self.REF_FORMATS)
                filesets[fileset.name] = fileset
        else:
            filesets = getattr(self, 'INPUT_FILESETS', None)
        self.add_session(filesets=filesets,
                         fields=getattr(self, 'INPUT_FIELDS', None))

    def add_session(self, filesets=None, fields=None, project_dir=None,
                    subject=None, visit=None):
        if project_dir is None:
            project_dir = self.project_dir
        if filesets is None:
            filesets = {}
        if subject is None:
            subject = self.SUBJECT
        if visit is None:
            visit = self.VISIT
        session_dir = op.join(project_dir, subject, visit)
        os.makedirs(session_dir)
        for name, fileset in list(filesets.items()):
            if isinstance(fileset, Fileset):
                if fileset.format is None:
                    raise ArcanaError(
                        "Need to provide format for fileset to add to test "
                        "dataset ({}) in {}".format(fileset, self))
                dst_path = op.join(session_dir,
                                   name + fileset.format.ext_str)
                if fileset.format.directory:
                    shutil.copytree(fileset.path, dst_path)
                else:
                    shutil.copy(fileset.path, dst_path)
            elif isinstance(fileset, basestring):
                # Write string as text file
                with open(op.join(session_dir,
                                  name + '.txt'), 'w') as f:
                    f.write(fileset)
            else:
                raise ArcanaError(
                    "Unrecognised fileset ({}) in {} test setup. Can "
                    "be either a Fileset or basestring object"
                    .format(fileset, self))
        if fields is not None:
            with open(op.join(session_dir,
                              LocalFileSystemRepo.FIELDS_FNAME), 'w',
                      **JSON_ENCODING) as f:
                json.dump(fields, f, indent=2)

    def delete_project(self, project_dir):
        # Clean out any existing dataset files
        shutil.rmtree(project_dir, ignore_errors=True)

    def reset_dirs(self):
        shutil.rmtree(self.project_dir, ignore_errors=True)
        shutil.rmtree(self.work_dir, ignore_errors=True)
        self.create_dirs()

    def create_dirs(self):
        for d in (self.project_dir, self.work_dir):
            if not op.exists(d):
                os.makedirs(d)

    @property
    def dataset_tree(self):
        return self.dataset.tree

    @property
    def xnat_session_name(self):
        return '{}_{}'.format(self.XNAT_TEST_PROJECT, self.name)

    @property
    def session_dir(self):
        return self.get_session_dir(self.SUBJECT, self.VISIT)

    def derived_session_dir(self, from_analysis=None):
        if from_analysis is None:
            from_analysis = self.STUDY_NAME
        return op.join(self.session_dir, from_analysis)

    @property
    def session(self):
        return self.dataset_tree.subject(
            self.SUBJECT).session(self.VISIT)

    @property
    def filesets(self):
        return self.session.filesets

    @property
    def fields(self):
        return self.session.fields

    @property
    def dataset(self):
        return self.local_dataset

    @property
    def local_dataset(self):
        try:
            return self._local_dataset
        except AttributeError:
            self._local_dataset = Dataset(self.project_dir, depth=2)
            return self._local_dataset

    @property
    def processor(self):
        return SingleProc(self.work_dir)

    @property
    def environment(self):
        return StaticEnv()

    @property
    def project_dir(self):
        return op.join(self.dataset_path, self.name)

    @property
    def work_dir(self):
        return op.join(self.work_path, self.name)

    @property
    def cache_dir(self):
        return op.join(self.cache_path, self.name)

    @property
    def ref_dir(self):
        return op.join(self.ref_path, self.name)

    @property
    def name(self):  # @NoSelf
        return self._get_name(type(self))

    @property
    def project_id(self):
        return self.name  # To allow override in deriving classes

    @classmethod
    def _get_name(cls, name_cls=None, sep='_'):
        """
        Get unique name for test class from module path and its class name to
        be used for storing test data on XNAT and creating unique work/project
        dirs
        """
        if name_cls is None:
            name_cls = cls
        module_path = op.abspath(sys.modules[name_cls.__module__].__file__)
        rel_module_path = module_path[(len(name_cls.unittest_root) + 1):]
        path_parts = rel_module_path.split(op.sep)
        module_name = (''.join(path_parts[:-1])
                       + op.splitext(path_parts[-1])[0][5:]).upper()
        test_class_name = name_cls.__name__.upper()
        if test_class_name.startswith('TEST'):
            test_class_name = test_class_name[4:]
        return module_name + sep + test_class_name

    def create_analysis(self, analysis_cls, name, inputs, dataset=None,
                        processor=None, environment=None, **kwargs):
        """
        Creates a analysis using default dataset and processors.

        Parameters
        ----------
        analysis_cls : Analysis
            The class to initialise
        name : str
            Name of the analysis
        inputs : List[BaseSpecMixin]
            List of inputs to the analysis
        dataset : Dataset | None
            The dataset to use (a default local dataset is used if one
            isn't provided
        processor : Processor | None
            The processor to use (a default SingleProc is used if one
            isn't provided
        """
        if dataset is None:
            dataset = self.dataset
        if processor is None:
            processor = self.processor
        if environment is None:
            environment = self.environment
        return analysis_cls(
            name=name,
            dataset=dataset,
            processor=processor,
            environment=environment,
            inputs=inputs,
            **kwargs)

    def assertFilesetCreated(self, fileset):
        if isinstance(fileset, FilesetSlice):
            filesets = list(fileset)
        else:
            filesets = [fileset]
        not_created = []
        for f in filesets:
            if op.exists(f.path):
                not_created.append(f)
        self.assertTrue(
            not not_created,
            ("{} {} not created by unittest".format(
                ', '.join(str(f) for f in not_created),
                'were' if len(not_created) > 1 else 'was')))

    def assertContentsEqual(self, slce, reference, context=None):
        if isinstance(slce, Fileset):
            slce = [slce]
        if isinstance(reference, (basestring, int, float)):
            if len(slce) != 1:
                raise ArcanaUsageError(
                    "Multi-subject/visit collections cannot be compared"
                    " against a single contents string (list or dict "
                    "should be provided)")
            references = [str(reference)]
            filesets = list(slce)
        elif isinstance(reference, dict):
            references = []
            filesets = []
            for subj_id, subj_dct in reference.items():
                for visit_id, ref_value in subj_dct.items():
                    references.append(str(ref_value))
                    filesets.append(slce.item(subject_id=subj_id,
                                              visit_id=visit_id))
        elif isinstance(reference, (list, tuple)):
            references = [str(r) for r in reference]
            filesets = list(slce)
            if len(references) != len(filesets):
                raise ArcanaUsageError(
                    "Number of provided references ({}) does not match"
                    " size of slce ({})".format(len(references),
                                                len(filesets)))
        else:
            raise ArcanaUsageError(
                "Unrecognised format for reference ({})"
                .format(reference))
        for fileset, ref in zip(filesets, references):
            with open(fileset.path) as f:
                contents = f.read()
            msg = ("Contents of {} ({}) do not match reference ({})"
                   .format(fileset, contents, ref))
            if context is not None:
                msg += 'for ' + context
            self.assertEqual(contents, ref, msg)

    def assertCreated(self, fileset):
        self.assertTrue(
            os.path.exists(fileset.path),
            "{} was not created".format(fileset))

    def assertField(self, name, ref_value, from_analysis, subject=None,
                    visit=None, frequency='per_session',
                    to_places=None):
        esc_name = from_analysis + '_' + name
        output_dir = self.get_session_dir(subject, visit, frequency)
        try:
            with open(op.join(output_dir,
                              LocalFileSystemRepo.FIELDS_FNAME)) as f:
                fields = json.load(f)
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise ArcanaError(
                    "No fields were created by pipeline in analysis '{}'"
                    .format(from_analysis))
        try:
            value = fields[esc_name]
        except KeyError:
            raise ArcanaError(
                "Field '{}' was not created by pipeline in analysis '{}'. "
                "Created fields were ('{}')"
                .format(esc_name, from_analysis, "', '".join(fields)))
        msg = ("Field value '{}' for analysis '{}', {}, does not match "
               "reference value ({})".format(name, from_analysis, value,
                                             ref_value))
        if to_places is not None:
            self.assertAlmostEqual(
                value, ref_value, to_places,
                '{} to {} decimal places'.format(msg, to_places))
        else:
            self.assertEqual(value, ref_value, msg)

    def assertFilesetsEqual(self, fileset1, fileset2, error_msg=None):
        msg = "{} does not match {}".format(fileset1, fileset2)
        if msg is not None:
            msg += ':\n' + error_msg
        self.assertTrue(filecmp.cmp(fileset1.path, fileset2.path,
                                    shallow=False), msg=msg)

    def assertStatEqual(self, stat, fileset_name, target, from_analysis,
                        subject=None, visit=None,
                        frequency='per_session'):
        val = float(sp.check_output(
            'mrstats {} -output {}'.format(
                self.output_file_path(
                    fileset_name, from_analysis,
                    subject=subject, visit=visit,
                    frequency=frequency),
                stat),
            shell=True))
        self.assertEqual(
            val, target, (
                "{} value of '{}' ({}) does not equal target ({}) "
                "for subject {} visit {}"
                .format(stat, fileset_name, val, target,
                        subject, visit)))

    def assertImagesAlmostMatch(self, out, ref, mean_threshold,
                                stdev_threshold, from_analysis):
        out_path = self.output_file_path(out, from_analysis)
        ref_path = self.ref_file_path(ref)
        # Should probably look into ITK fuzzy matching methods
        cmd = ("mrcalc -quiet {a} {b} -subtract - | mrstats - | "
               "grep -v channel | awk '{{print $4 \" \" $6}}'"
               .format(a=out_path, b=ref_path))
        out = sp.check_output(cmd, shell=True)
        mean, stdev = (float(x) for x in out.split())
        self.assert_(
            abs(mean) < mean_threshold and stdev < stdev_threshold,
            ("Mean ({mean}) or standard deviation ({stdev}) of difference "
             "between images {a} and {b} differ more than threshold(s) "
             "({thresh_mean} and {thresh_stdev} respectively)"
             .format(mean=mean, stdev=stdev, thresh_mean=mean_threshold,
                     thresh_stdev=stdev_threshold, a=out_path, b=ref_path)))

    def get_session_dir(self, subject=None, visit=None,
                        frequency='per_session', from_analysis=None):
        if subject is None and frequency in ('per_session', 'per_subject'):
            subject = self.SUBJECT
        if visit is None and frequency in ('per_session', 'per_visit'):
            visit = self.VISIT
        if frequency == 'per_session':
            assert subject is not None
            assert visit is not None
            path = op.join(self.project_dir, subject, visit)
        elif frequency == 'per_subject':
            assert subject is not None
            assert visit is None
            path = op.join(
                self.project_dir, subject,
                LocalFileSystemRepo.SUMMARY_NAME)
        elif frequency == 'per_visit':
            assert visit is not None
            assert subject is None
            path = op.join(self.project_dir,
                           LocalFileSystemRepo.SUMMARY_NAME, visit)
        elif frequency == 'per_dataset':
            assert subject is None
            assert visit is None
            path = op.join(self.project_dir,
                           LocalFileSystemRepo.SUMMARY_NAME,
                           LocalFileSystemRepo.SUMMARY_NAME)
        else:
            assert False
        if from_analysis is not None:
            path = op.join(path, from_analysis)
        return op.abspath(path)

    def remove_generated_files(self, analysis=None):
        # Remove derived filesets
        for fname in os.listdir(self.get_session_dir()):
            if analysis is None or fname.startswith(analysis + '_'):
                os.remove(op.join(self.get_session_dir(), fname))

    def output_file_path(self, fname, from_analysis, subject=None, visit=None,
                         frequency='per_session', **kwargs):
        return op.join(
            self.get_session_dir(subject=subject, visit=visit,
                                 frequency=frequency,
                                 from_analysis=from_analysis, **kwargs),
            fname)

    def ref_file_path(self, fname, subject=None, session=None):
        return op.join(self.session_dir, fname)


class BaseMultiSubjectTestCase(BaseTestCase):

    SUMMARY_NAME = LocalFileSystemRepo.SUMMARY_NAME
    DATASET_CONTENTS = None
    input_tree = None

    def setUp(self):
        self.reset_dirs()
        self.add_sessions()

    def add_sessions(self):
        self.local_tree = deepcopy(self.input_tree)
        for node in self.local_tree:
            for fileset in node.filesets:
                fileset._dataset = self.local_dataset
                fileset._path = op.join(
                    fileset.dataset.repository.fileset_path(fileset))
                session_path = op.dirname(fileset.path)
                self._make_dir(session_path)
                contents = self.DATASET_CONTENTS[fileset.name]
                if fileset.format.aux_files:
                    fileset._aux_files = {}
                    for (aux_name,
                         aux_path) in fileset.format.default_aux_file_paths(
                            fileset._path).items():
                        fileset._aux_files[aux_name] = aux_path
                        with open(aux_path, 'w') as f:
                            f.write(str(contents[aux_name]))
                    contents = contents['.']
                with open(fileset.path, 'w') as f:
                    f.write(str(contents))
                if fileset.derived:
                    self._make_dir(op.join(session_path,
                                           LocalFileSystemRepo.PROV_DIR))
            for field in node.fields:
                fields_path = self.local_dataset.repository.fields_json_path(
                    field, self.local_dataset)
                if op.exists(fields_path):
                    with open(fields_path, **JSON_ENCODING) as f:
                        dct = json.load(f)
                else:
                    if not op.exists(op.dirname(fields_path)):
                        os.makedirs(op.dirname(fields_path))
                    dct = {}
                dct[field.name] = field.value
                with open(fields_path, 'w', **JSON_ENCODING) as f:
                    json.dump(dct, f, indent=2)
                if field.derived:
                    self._make_dir(op.join(session_path,
                                           LocalFileSystemRepo.PROV_DIR))

    @property
    def subject_ids(self):
        return (d for d in os.listdir(self.project_dir)
                if d != self.SUMMARY_NAME)

    def visit_ids(self, subject_id):
        subject_dir = op.join(self.project_dir, subject_id)
        return (d for d in os.listdir(subject_dir)
                if d != self.SUMMARY_NAME)

    def session_dir(self, subject, visit):
        return self.get_session_dir(subject, visit)

    def get_session_dir(self, subject, visit, **kwargs):
        return super(BaseMultiSubjectTestCase, self).get_session_dir(
            subject=subject, visit=visit, **kwargs)

    def _make_dir(self, path):
        makedirs(path, exist_ok=True)
        return path


class DummyTestCase(BaseTestCase):

    def __init__(self):
        self.setUp()

    def __del__(self):
        self.tearDown()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_(self, statement, message=None):
        if not statement:
            message = "'{}' is not true".format(statement)
            print(message)
        else:
            print("Test successful")

    def assertEqual(self, first, second, message=None):
        if first != second:
            if message is None:
                message = '{} and {} are not equal'.format(repr(first),
                                                           repr(second))
            print(message)
        else:
            print("Test successful")

    def assertAlmostEqual(self, first, second, message=None):
        if first != second:
            if message is None:
                message = '{} and {} are not equal'.format(repr(first),
                                                           repr(second))
            print(message)
        else:
            print("Test successful")

    def assertLess(self, first, second, message=None):
        if first >= second:
            if message is None:
                message = '{} is not less than {}'.format(repr(first),
                                                          repr(second))
            print(message)
        else:
            print("Test successful")
