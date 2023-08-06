"""
This will run the whole pipeline

v0.02
"""
import scripts.create_metadata_file as create_metadata_file
import scripts.post_process_test as post_process_tests
import scripts.process_and_load as process_and_load
import scripts.raw_data_analysis as raw_data_analysis
import scripts.preprocessing_checks as preprocessor_checks

from loguru import logger


def main(processing_steps):
    run_step = {
        'analyze_dataset': raw_data_analysis.analyze_dataset(),
        'preprocessor_checks': preprocessor_checks.preprocessor_checks(''),
        'process_and_load_data': process_and_load.process_and_load_data(),
        'create_metadata_file_structure': create_metadata_file.create_metadata_file_structure(''),
        'check_database': post_process_tests.check_database(),
        'check_metadata': post_process_tests.check_metadata(),
        'check_database_metadata': post_process_tests.check_database_metadata(),
    }

    for step in processing_steps:
        logger.info(f'Running step {step}'.center(20, '🐍'))
        run_step[step]


if __name__ == '__main__':
    steps = {
        'analyze_dataset',
        'process_and_load_data',
        'create_metadata_file_structure',
        'check_database',
        'check_metadata',
        'check_database_metadata',
    }

    main(steps)
