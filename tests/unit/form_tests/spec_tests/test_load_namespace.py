import unittest
import tempfile
import ruamel.yaml as yaml
import json

from form.spec import *

class TestSpecLoad(unittest.TestCase):
    NS_NAME = 'test_ns'

    def setUp(self):
        self.attributes = [
            AttributeSpec('attribute1', 'str', 'my first attribute'),
            AttributeSpec('attribute2', 'str', 'my second attribute')
        ]
        self.dset1_attributes = [
            AttributeSpec('attribute3', 'str', 'my third attribute'),
            AttributeSpec('attribute4', 'str', 'my fourth attribute')
        ]
        self.dset2_attributes = [
            AttributeSpec('attribute5', 'str', 'my fifth attribute'),
            AttributeSpec('attribute6', 'str', 'my sixth attribute')
        ]
        self.datasets = [
            DatasetSpec('my first dataset',
                        'int',
                        name='dataset1',
                        attributes=self.dset1_attributes,
                        linkable=True),
            DatasetSpec('my second dataset',
                        'int',
                        name='dataset2',
                        dimension=(None, None),
                        attributes=self.dset2_attributes,
                        linkable=True,
                        data_type_def='VoltageArray')
        ]
        self.spec = GroupSpec('A test group',
                         name='root_constructor_nwbtype',
                         datasets=self.datasets,
                         attributes=self.attributes,
                         linkable=False,
                         data_type_def='EphysData')
        dset1_attributes_ext = [
            AttributeSpec('dset1_extra_attribute', 'str', 'an extra attribute for the first dataset')
        ]
        self.ext_datasets = [
            DatasetSpec('my first dataset extension',
                        'int',
                        name='dataset1',
                        attributes=dset1_attributes_ext,
                        linkable=True),
        ]
        self.ext_attributes = [
            AttributeSpec('ext_extra_attribute', 'str', 'an extra attribute for the group'),
        ]
        self.ext_spec =  GroupSpec('A test group extension',
                            name='root_constructor_nwbtype',
                            datasets=self.ext_datasets,
                            attributes=self.ext_attributes,
                            linkable=False,
                            data_type_inc='EphysData',
                            data_type_def='SpikeData')
        to_dump = {'groups': [self.spec, self.ext_spec]}
        self.specs_path = 'test_load_namespace.specs.yaml'
        self.namespace_path = 'test_load_namespace.namespace.yaml'
        with open(self.specs_path, 'w') as tmp:
            yaml.dump(json.loads(json.dumps(to_dump)), tmp, default_flow_style=False)
        ns_dict = {
            'doc': 'a test namespace',
            'name': self.NS_NAME,
            'schema': [
                { 'source': self.specs_path }
            ]
        }
        self.namespace = SpecNamespace.build_namespace(**ns_dict)
        to_dump = {'namespaces': [self.namespace]}
        with open(self.namespace_path, 'w') as tmp:
            yaml.dump(json.loads(json.dumps(to_dump)), tmp, default_flow_style=False)
        self.ns_catalog = NamespaceCatalog(self.NS_NAME)

    def tearDown(self):
        if os.path.exists(self.namespace_path):
            os.remove(self.namespace_path)
        if os.path.exists(self.specs_path):
            os.remove(self.specs_path)

    def test_inherited_attributes(self):
        self.ns_catalog.load_namespaces(self.namespace_path, resolve=True)
        ts_spec = self.ns_catalog.get_spec(self.NS_NAME, 'EphysData')
        es_spec = self.ns_catalog.get_spec(self.NS_NAME, 'SpikeData')
        ts_attrs = { s.name for s in ts_spec.attributes }
        es_attrs = { s.name for s in es_spec.attributes }
        for attr in ts_attrs:
            with self.subTest(attr=attr):
                self.assertIn(attr, es_attrs)
        #self.assertSetEqual(ts_attrs, es_attrs)
        ts_dsets = { s.name for s in ts_spec.datasets }
        es_dsets = { s.name for s in es_spec.datasets }
        for dset in ts_dsets:
            with self.subTest(dset=dset):
                self.assertIn(dset, es_dsets)
        #self.assertSetEqual(ts_dsets, es_dsets)


    def test_inherited_attributes_not_resolved(self):
        self.ns_catalog.load_namespaces(self.namespace_path, resolve=False)
        es_spec = self.ns_catalog.get_spec(self.NS_NAME, 'SpikeData')
        src_attrs = { s.name for s in self.ext_attributes }
        ext_attrs = { s.name for s in es_spec.attributes }
        self.assertSetEqual(src_attrs, ext_attrs)
        src_dsets = { s.name for s in self.ext_datasets }
        ext_dsets = { s.name for s in es_spec.datasets }
        self.assertSetEqual(src_dsets, ext_dsets)

