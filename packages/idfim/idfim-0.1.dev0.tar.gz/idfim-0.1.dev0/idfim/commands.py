#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2019 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Command line tools.
"""

import argparse
import sys

import idfim.io.idfmapi
import idfim.io.config
import idfim.io.data
import idfim.io.html
import idfim.idfmapirequest


DEFAULT_CONFIG_PATH = "~/.idfim.yaml"
DEFAULT_DATA_PATH = "~/idfim_data.json"
DEFAULT_HTML_PATH = "~/idfim_html"


def fetch_isochrone_maps_from_domiciles_to_workplaces(api_token, config_dict, data, data_path):

    date_list = config_dict["dates_list"]
    time_list = config_dict["domicile_to_workplace_hours"]
    max_duration_list = config_dict["isochrone_journey_duration"]

    print("Starting points:", [pt["label"] for pt in config_dict['domiciles'].values()])
    print("Date list:", date_list)
    print("Time list:", time_list)
    print("Max duration list:", max_duration_list)

    for starting_point_gps in config_dict['domiciles']:
        for date_str in date_list:
            for time_str in time_list:
                for max_duration in max_duration_list:
                    if starting_point_gps not in data['domiciles']:
                        data['domiciles'][starting_point_gps] = config_dict['domiciles'][starting_point_gps]
                    starting_point = data['domiciles'][starting_point_gps]

                    if (date_str in starting_point) and (time_str in starting_point[date_str]) and (str(max_duration) in starting_point[date_str][time_str]):
                        print("Skip", starting_point["label"], date_str, time_str, max_duration, "(already fetched)")
                    else:
                        print(starting_point["label"], date_str, time_str, max_duration)

                        hour, minute = time_str.split(":")
                        year, month, day = date_str.split("-")

                        isochrone_polygon = idfim.idfmapirequest.get_isochrone_polygon(api_token=api_token,
                                                                             starting_point=starting_point_gps,
                                                                             max_duration=int(max_duration),
                                                                             datetime="{}{}{}T{}{}00".format(year, month, day, hour, minute))

                        if date_str not in starting_point:
                            starting_point[date_str] = {}

                        if time_str not in starting_point[date_str]:
                            starting_point[date_str][time_str] = {}

                        starting_point[date_str][time_str][str(max_duration)] = isochrone_polygon

                        # Save data
                        idfim.io.data.save_data(data, data_path=data_path)


def fetch_isochrone_maps_from_workplaces_to_domiciles(api_token, config_dict, data, data_path):

    date_list = config_dict["dates_list"]
    time_list = config_dict["workplace_to_domicile_hours"]
    max_duration_list = config_dict["isochrone_journey_duration"]

    print("Starting points:", [pt["label"] for pt in config_dict['workplaces'].values()])
    print("Date list:", date_list)
    print("Time list:", time_list)
    print("Max duration list:", max_duration_list)

    for starting_point_gps in config_dict['workplaces']:
        for date_str in date_list:
            for time_str in time_list:
                for max_duration in max_duration_list:
                    if starting_point_gps not in data['workplaces']:
                        data['workplaces'][starting_point_gps] = config_dict['workplaces'][starting_point_gps]
                    starting_point = data['workplaces'][starting_point_gps]

                    if (date_str in starting_point) and (time_str in starting_point[date_str]) and (str(max_duration) in starting_point[date_str][time_str]):
                        print("Skip", starting_point["label"], date_str, time_str, max_duration, "(already fetched)")
                    else:
                        print(starting_point["label"], date_str, time_str, max_duration)

                        hour, minute = time_str.split(":")
                        year, month, day = date_str.split("-")

                        isochrone_polygon = idfim.idfmapirequest.get_isochrone_polygon(api_token=api_token,
                                                                             starting_point=starting_point_gps,
                                                                             max_duration=int(max_duration),
                                                                             datetime="{}{}{}T{}{}00".format(year, month, day, hour, minute))

                        if date_str not in starting_point:
                            starting_point[date_str] = {}

                        if time_str not in starting_point[date_str]:
                            starting_point[date_str][time_str] = {}

                        starting_point[date_str][time_str][str(max_duration)] = isochrone_polygon

                        # Save data
                        idfim.io.data.save_data(data, data_path=data_path)


def main():
    """Main function"""

    # Parse arguments ###############################################

    parser = argparse.ArgumentParser(description='Make an isochrone map of Paris region using public transportation.')

    parser.add_argument("--config", "-c", default=DEFAULT_CONFIG_PATH, metavar="STRING",
            help="Configuration file path [default: {}]".format(DEFAULT_CONFIG_PATH))

    parser.add_argument("--data", "-d", default=DEFAULT_DATA_PATH, metavar="STRING",
            help="Data file path [default: {}]".format(DEFAULT_DATA_PATH))

    parser.add_argument("--html", "-o", default=DEFAULT_HTML_PATH, metavar="STRING",
            help="Output html path [default: {}]".format(DEFAULT_HTML_PATH))

    parser.add_argument("--data-only", "-D", action="store_true",
            help="Only fetch data (don't make HTML output files)")

    parser.add_argument("--html-only", "-H", action="store_true",
            help="Only make HTML output files (don't fetch data)")

    #parser.add_argument("--help", "-h", action="store_true",
    #        help="Display the command line options and exit")

    parser.add_argument("--version", "-v", action="store_true",
            help="Output version information and exit")

    args = parser.parse_args()

    if args.version:
        print(idfim.get_version())
        sys.exit(0)

    config_path = args.config
    data_path = args.data
    html_path = args.html
    data_only = args.data_only
    html_only = args.html_only

    # Make isochrone maps ###########################################

    try:
        if data_only and html_only:
            raise Exception("Error: --data-only and --html-only options are not compatible.")

        # Get config params #############################################

        config_dict = idfim.io.config.load_config(config_path=config_path)

        # Load data #####################################################

        data = idfim.io.data.load_data(data_path=data_path)

        if (data is None) or (data == {}):
            data = {}
            data['domiciles'] = config_dict['domiciles']
            data['workplaces'] = config_dict['workplaces']

        # Fetch data ####################################################

        if not html_only:
            # Get credentials
            api_token = idfim.io.idfmapi.get_idfm_journey_planner_app_api_token()

            fetch_isochrone_maps_from_domiciles_to_workplaces(api_token, config_dict, data, data_path)
            fetch_isochrone_maps_from_workplaces_to_domiciles(api_token, config_dict, data, data_path)

            ## Save data
            #idfim.io.data.save_data(data, data_path=data_path)

        # Save html #####################################################

        if not data_only:
            idfim.io.html.data_to_html(data, html_dir_path=html_path)

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
