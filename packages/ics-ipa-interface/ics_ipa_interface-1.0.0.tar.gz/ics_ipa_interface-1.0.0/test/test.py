import ics_ipa_interface as ipa


if __name__ == '__main__':
    # setup the help dialog for the script
    ipa.ipa_init(script_name='my_script_name.py', version='1.0',
                 message='this dose cool things')

    # input data path
    data_file_paths = ipa.get_data_files()
    if data_file_paths != ['datafile1', 'datafile2']:
        raise 'data files did not match'

    # config are user defined and are uses as arguments to
    # the script
    config_file_paths = ipa.get_config_files()
    if config_file_paths != ['config1', 'config2']:
        raise 'config files did not match'

    # path to store data
    output_path = ipa.get_output_dir()
    if output_path != 'outputDir':
        raise 'output dir did not match'

    vehicle = ipa.get_data_attribute_from_ipa_file(data_file_paths[0], 'vehicleId')
    if not ipa.using_ipa_file() and vehicle is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and vehicle != 1234:
        raise 'did not read value properly'

    vehicle = ipa.get_data_attribute_from_ipa_file(data_file_paths[1], 'vehicleId')
    if not ipa.using_ipa_file() and vehicle is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and vehicle is not None:
        raise 'did not read value properly'
