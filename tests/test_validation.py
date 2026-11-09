import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate_actuome import check_schema_subset, load_json, validate_profile
from tools.profile_report import make_report


@contextmanager
def local_test_file():
    # Stay inside the checkout on systems whose temporary directory is restricted.
    with tempfile.NamedTemporaryFile(dir=ROOT, prefix='.actuome-test-', suffix='.json', delete=False) as handle:
        path = Path(handle.name).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise RuntimeError('Test file escaped the checkout')
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)


class ProfileValidationTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_json(ROOT / 'examples/demo_bench.synthetic.json')

    def assert_invalid(self, data=None, contains=None, **options):
        result = validate_profile(data or self.profile, **options)
        self.assertFalse(result['valid'], result)
        if contains:
            self.assertIn(contains, ' '.join(result['errors']))

    def test_all_shipped_examples_are_valid_but_not_physically_verified(self):
        for path in (ROOT / 'examples').glob('*.json'):
            with self.subTest(path=path.name):
                result = validate_profile(load_json(path))
                self.assertTrue(result['valid'], result)
                self.assertFalse(result['physical_measurements_verified'])

    def test_measured_only_rejects_synthetic(self):
        self.assert_invalid(contains='measured-only', measured_only=True)

    def test_missing_manufacturer(self):
        del self.profile['platform']['manufacturer']
        self.assert_invalid(contains='manufacturer')

    def test_unknown_field_rejected(self):
        self.profile['axes'][0]['latency']['claimed_score'] = 99
        self.assert_invalid(contains='unknown field')

    def test_unknown_version_rejected(self):
        self.profile['actuome_version'] = '0.2.0'
        self.assert_invalid(contains='0.1.0')

    def test_boolean_not_a_number(self):
        self.profile['axes'][0]['limits']['continuous_effort'] = True
        self.assert_invalid()

    def test_empty_axes_rejected(self):
        self.profile['axes'] = []
        self.assert_invalid(contains='too few')

    def test_wrong_rotary_units(self):
        self.profile['axes'][0]['effort_unit'] = 'N'
        self.assert_invalid(contains='units')

    def test_wrong_linear_units(self):
        self.profile['axes'][1]['velocity_unit'] = 'rad/s'
        self.assert_invalid(contains='units')

    def test_complete_coverage_must_match_dof(self):
        self.profile['platform']['total_actuated_dof'] = 28
        self.assert_invalid(contains='Complete coverage')

    def test_partial_coverage_must_actually_be_partial(self):
        self.profile['coverage'] = 'partial'
        self.assert_invalid(contains='Partial coverage')

    def test_duplicate_axis_id(self):
        self.profile['axes'][1]['axis_id'] = self.profile['axes'][0]['axis_id']
        self.assert_invalid(contains='duplicate axis_id')

    def test_multiple_axes_may_share_joint_name(self):
        self.profile['axes'][1]['joint_name'] = self.profile['axes'][0]['joint_name']
        self.assertTrue(validate_profile(self.profile)['valid'])

    def test_bad_interface_reference(self):
        self.profile['axes'][0]['interface_ref'] = 'missing-bus'
        self.assert_invalid(contains='interface_ref')

    def test_bad_source_reference(self):
        self.profile['axes'][0]['evidence']['source_refs'] = ['missing-source']
        self.assert_invalid(contains='unknown evidence source')

    def test_negative_latency(self):
        self.profile['axes'][0]['latency']['median_ms'] = -1
        self.assert_invalid()

    def test_latency_quantiles_out_of_order(self):
        self.profile['axes'][0]['latency']['p95_ms'] = 1
        self.assert_invalid(contains='quantiles')

    def test_peak_below_continuous(self):
        self.profile['axes'][0]['limits']['peak_effort'] = 1
        self.assert_invalid(contains='peak effort is below')

    def test_peak_without_duration(self):
        self.profile['axes'][0]['limits']['peak_duration_s'] = None
        self.assert_invalid(contains='burst duration')

    def test_reference_velocity_above_envelope(self):
        self.profile['axes'][0]['limits']['continuous_effort_at_velocity'] = 20
        self.assert_invalid(contains='reference velocity')

    def test_curve_speed_must_be_ordered(self):
        self.profile['axes'][0]['effort_speed_curve'].reverse()
        self.assert_invalid(contains='strictly increasing')

    def test_curve_exceeds_envelope(self):
        self.profile['axes'][0]['effort_speed_curve'][0]['continuous_effort'] = 100
        self.assert_invalid(contains='continuous effort envelope')

    def test_thermal_fraction_out_of_range(self):
        self.profile['axes'][0]['thermal']['derating_curve'][0]['effort_fraction'] = 2
        self.assert_invalid(contains='maximum')

    def test_measured_label_needs_metadata_and_real_source_kind(self):
        for axis in self.profile['axes']:
            axis['evidence']['basis'] = 'measured'
        self.profile['data_status'] = 'measured'
        self.assert_invalid(contains='measured evidence requires')

    def measured_test_declaration(self):
        # Unit-test-only metadata, not an experimental result or published profile.
        data = copy.deepcopy(self.profile)
        data['data_status'] = 'measured'
        data['sources'][0]['kind'] = 'measurement_report'
        for axis in data['axes']:
            axis['evidence'].update({
                'basis': 'measured', 'measured_at': '2026-11-09T12:00:00+03:00',
                'sample_count': 200, 'instrument': 'Fictional test fixture',
                'uncertainty_note': 'Unit-test declaration only; no experiment performed.'
            })
        return data

    def test_complete_measurement_declaration_passes_without_verifying_truth(self):
        result = validate_profile(self.measured_test_declaration(), measured_only=True)
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['physical_measurements_verified'])

    def test_measurement_timestamp_requires_timezone(self):
        data = self.measured_test_declaration()
        data['axes'][0]['evidence']['measured_at'] = '2026-11-09T12:00:00'
        self.assert_invalid(data, contains='timezone')

    def test_status_cannot_hide_synthetic_axes(self):
        self.profile['data_status'] = 'measured'
        self.assert_invalid(contains='data_status')

    def test_unknown_template_cannot_assert_numbers(self):
        data = load_json(ROOT / 'examples/unmeasured.template.json')
        data['axes'][0]['latency'].update({'boundary': 'control_bus_only', 'median_ms': 1})
        self.assert_invalid(data, contains='unknown evidence')

    def test_nan_infinite_and_duplicate_json_are_rejected(self):
        with local_test_file() as path:
            for content in ('{"x":NaN}', '{"x":Infinity}', '{"x":1,"x":2}'):
                path.write_text(content, encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_json(path)

    def test_arbitrary_new_schema_keyword_fails_closed(self):
        with self.assertRaises(ValueError):
            check_schema_subset({'type': 'object', 'unevaluatedProperties': False})

    def test_export_is_labelled_synthetic_and_unverified(self):
        text = make_report(self.profile)
        self.assertIn('synthetic', text)
        self.assertIn('NOT been independently verified', text)
        self.assertIn('N*m', text)
        self.assertIn('m/s', text)

    def test_export_rejects_invalid_input(self):
        self.profile['platform']['total_actuated_dof'] = 28
        with self.assertRaises(ValueError):
            make_report(self.profile)

    def test_cli_success_and_measured_gate_exit_codes(self):
        command = [sys.executable, str(ROOT / 'validate_actuome.py'),
                   str(ROOT / 'examples/demo_bench.synthetic.json'), '--json']
        good = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertTrue(json.loads(good.stdout)['valid'])
        rejected = subprocess.run(command + ['--measured-only'], capture_output=True, text=True)
        self.assertEqual(rejected.returncode, 1)
        self.assertFalse(json.loads(rejected.stdout)['valid'])

    def test_cli_bad_json_is_clean_failure(self):
        with local_test_file() as path:
            path.write_text('{broken', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'validate_actuome.py'), str(path), '--json'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['valid'])
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
