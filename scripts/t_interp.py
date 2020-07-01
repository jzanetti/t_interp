
import argparse
from utils import utils
from interp import temporal_interp_wrapper
from data import read_data
from vis import plot_wrapper


def main(data_path, out_dir, output_prefix, target_interval_min, generate_plot):
    
    dirs = utils.create_dirs(out_dir)
    datapath_config = utils.read_datapath(data_path)

    forecasts, data_mask, latitude, longitude, valid_times = \
        read_data.read_data(datapath_config)

    start_time, end_time = utils.get_datetime_range(valid_times)

    temporal_interp_wrapper.t_interp_wrapper(
        start_time, end_time, valid_times, dirs['output'],
        output_prefix, 
        forecasts, data_mask, latitude, longitude, 
        target_interval_min)

    if generate_plot:
        plot_wrapper.plot_wrapper(output_prefix, dirs['figure'],
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
                        help='data path to be temporal downscaled '
                             '(datapath list)')
    parser.add_argument('--output_prefix', type=str, required=False,
                        default='raincast', help='data name to be '
                        'output, e.g., raincast_det')
    parser.add_argument('--output_dir', type=str, required=True, 
                        help='output data directory')
    parser.add_argument('--generate_plot', help='if produce plots',
                        action='store_true')
    parser.add_argument('--target_interval_min', type=str, required=False,
                        default='10', help='temporal resolution '
                        'to be interpolated')

    return parser.parse_args(
        ['--data_path', '/home/szhang/eclipse-workspace/temporal_interp/etc/raincast_interp.yaml',
         '--output_prefix', 'raincast', '--output_dir', '/tmp/t_interp',
         # '--generate_plot'
        ])


if __name__ == '__main__':
    args = setup_parser()
    main(args.data_path, args.output_dir, 
         args.output_prefix, int(args.target_interval_min),
         args.generate_plot)


