from unittest.mock import MagicMock, patch

from scaaml.aes_forward import AESSBOX
from scaaml.capture.aes.crypto_alg import SCryptoAlgorithm
from scaaml.io import resume_kti


@patch.object(resume_kti, 'create_resume_kti')
@patch.object(resume_kti, 'ResumeKTI')
def test_init(mock_resumekti, mock_create_resume_kti):
    description = 'train'
    implementation = 'MBEDTLS'
    algorithm = 'simpleserial-aes'
    keys = 3072
    plaintexts = 256
    repetitions = 1
    examples_per_shard = 64
    firmware_sha256 = 'TODO'
    full_kt_filename = 'ktfilename.txt'
    full_progress_filename = 'progressfilename.txt'

    crypto_alg = SCryptoAlgorithm(
        crypto_implementation=AESSBOX,
        purpose=description,
        implementation=implementation,
        algorithm=algorithm,
        keys=keys,
        plaintexts=plaintexts,
        repetitions=repetitions,
        examples_per_shard=examples_per_shard,
        firmware_sha256=firmware_sha256,
        full_kt_filename=full_kt_filename,
        full_progress_filename=full_progress_filename)

    mock_create_resume_kti.assert_called_once()
    kwargs = mock_create_resume_kti.call_args.kwargs
    assert kwargs['shard_length'] == examples_per_shard
    assert kwargs['kt_filename'] == full_kt_filename
    assert kwargs['progress_filename'] == full_progress_filename
    assert crypto_alg.examples_per_shard == examples_per_shard
    assert crypto_alg.keys == keys
    assert crypto_alg.plaintexts == plaintexts
    assert crypto_alg.repetitions == repetitions
    assert crypto_alg.key_len == 16
    stab_kti = crypto_alg.get_stabilization_kti()
    stab_k, stab_t = next(stab_kti)
    assert crypto_alg.key_len == len(stab_k)
    assert crypto_alg.plaintext_len == 16
    assert crypto_alg.plaintext_len == len(stab_t)
    assert crypto_alg.firmware_sha256 == firmware_sha256
    assert crypto_alg.implementation == implementation
    assert crypto_alg.algorithm == algorithm
    assert crypto_alg.purpose == description


@patch.object(resume_kti, 'create_resume_kti')
@patch.object(resume_kti, 'ResumeKTI')
def test_attack_points(mock_resumekti, mock_create_resume_kti):
    description = 'train'
    implementation = 'MBEDTLS'
    algorithm = 'simpleserial-aes'
    keys = 3072
    plaintexts = 256
    repetitions = 1
    examples_per_shard = 64
    firmware_sha256 = 'TODO'
    full_kt_filename = 'ktfilename.txt'
    full_progress_filename = 'progressfilename.txt'
    crypto_alg = SCryptoAlgorithm(
        crypto_implementation=AESSBOX,
        purpose=description,
        implementation=implementation,
        algorithm=algorithm,
        keys=keys,
        plaintexts=plaintexts,
        repetitions=repetitions,
        examples_per_shard=examples_per_shard,
        firmware_sha256=firmware_sha256,
        full_kt_filename=full_kt_filename,
        full_progress_filename=full_progress_filename)
    key = bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    plaintext = bytearray(
        [255, 254, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    ap = {
        'sub_bytes_in': AESSBOX.sub_bytes_in(key=key, plaintext=plaintext),
        'sub_bytes_out': AESSBOX.sub_bytes_out(key=key, plaintext=plaintext),
        'key': key,
    }
    assert crypto_alg.attack_points(key=key, plaintext=plaintext) == ap


@patch.object(resume_kti, 'create_resume_kti')
@patch.object(resume_kti, 'ResumeKTI')
def test_attack_points_info(mock_resumekti, mock_create_resume_kti):
    description = 'train'
    implementation = 'MBEDTLS'
    algorithm = 'simpleserial-aes'
    keys = 3072
    plaintexts = 256
    repetitions = 1
    examples_per_shard = 64
    firmware_sha256 = 'TODO'
    full_kt_filename = 'ktfilename.txt'
    full_progress_filename = 'progressfilename.txt'
    crypto_alg = SCryptoAlgorithm(
        crypto_implementation=AESSBOX,
        purpose=description,
        implementation=implementation,
        algorithm=algorithm,
        keys=keys,
        plaintexts=plaintexts,
        repetitions=repetitions,
        examples_per_shard=examples_per_shard,
        firmware_sha256=firmware_sha256,
        full_kt_filename=full_kt_filename,
        full_progress_filename=full_progress_filename)
    max_val = 256
    api = {
        'sub_bytes_in': {
            'len': 16,
            'max_val': max_val,
        },
        'sub_bytes_out': {
            'len': 16,
            'max_val': max_val,
        },
        'key': {
            'len': 16,
            'max_val': max_val,
        }
    }
    assert crypto_alg.attack_points_info() == api
