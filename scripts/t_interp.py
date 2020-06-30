
import argparse
from utils import utils
from interp import temporal_interp_wrapper
from data import read_data
from vis import plot_wrapper


def main(data_path, out_dir, datatype, target_interval_min, generate_plot):
    
    dirs = utils.create_dirs(out_dir)
    forecasts, data_mask, latitude, longitude, valid_times = \
        read_data.read_data(data_path, datatype)

    start_time, end_time = utils.get_datetime_range(valid_times)

    temporal_interp_wrapper.t_interp_wrapper(
        start_time, end_time, valid_times, dirs['output'], datatype, 
        forecasts, data_mask, latitude, longitude, 
        target_interval_min)

    if generate_plot:
        plot_wrapper.plot_wrapper(datatype, dirs['figure'],
                                  dirs['output'], start_time, end_time)


def get_example_usage():
    example_text = '''example:
        * t_interp.py  --data_path /tmp/raincast_det.nc
                       --data_type raincast_det
                       --output_dir /tmp/t_interp
                       --generate_plot
                       [--target_interval_min 10]
         '''
    return example_text


def setup_parser():
    # -----------------------
    # required (basic)
    # -----------------------
    parser = argparse.ArgumentParser(
        description='temporal interpolation program',
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--data_path', type=str, required=True, 
                        help='data path to be temporal downscaled')
    parser.add_argument('--data_type', type=str, required=False,
                        default='raincast_det', help='data type to be '
                        'downscaled, e.g., raincast_det')
    parser.add_argument('--output_dir', type=str, required=True, 
                        help='output data directory')
    parser.add_argument('--generate_plot', help='if produce plots',
                        action='store_true')
    parser.add_argument('--target_interval_min', type=str, required=False,
                        default='10', help='temporal resolution '
                        'to be interpolated')

    return parser.parse_args(
        ['--data_path', '/home/szhang/Downloads/raincast_determinstic_202006292200.nc',
         '--data_type', 'raincast_det', '--output_dir', '/tmp/t_interp',
         '--generate_plot'])


if __name__ == '__main__':
    args = setup_parser()
    main(args.data_path, args.output_dir, 
         args.data_type, int(args.target_interval_min),
         args.generate_plot)


