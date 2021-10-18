import json


def create_global_config_args(
    project_loc,
    sim_name,
    start_run,
    end_run,
    commodity_list,
    # start_commodity,
    # end_commodity,
    country_of_interest,
    native_countries_list,
    start_years,
    alphas,
    betas,
    lamdas,
    transmission_lag_type,
    gamma_shape,
    gamma_scale,
    threshold_val,
    scaled_min,
    scaled_max,
    season_dict,
    timestep,
    years_before_firstRecord,
    years_after_firstRecord,
    end_valid_year,
    sim_years,
):

    args = {}

    # Directory and file paths
    args["project_loc"] = project_loc
    args["sim_name"] = sim_name
    args["start_run"] = start_run
    args["end_run"] = end_run
    args['commodity_list'] = commodity_list
    # args["start_commodity"] = start_commodity
    # args["end_commodity"] = end_commodity
    args["country_of_interest"] = country_of_interest
    args["native_countries_list"] = native_countries_list
    args["start_years"] = start_years
    args["alphas"] = alphas
    args["lamdas"] = lamdas
    args["betas"] = betas
    args["transmission_lag_type"] = transmission_lag_type
    args["gamma_shape"] = gamma_shape
    args["gamma_scale"] = gamma_scale
    args["threshold_val"] = threshold_val
    args["scaled_min"] = scaled_min
    args["scaled_max"] = scaled_max
    args["season_dict"] = season_dict
    args["timestep"] = timestep
    args["years_before_firstRecord"] = years_before_firstRecord
    args["years_after_firstRecord"] = years_after_firstRecord
    args["end_valid_year"] = end_valid_year
    args["sim_years"] = sim_years

    # Write arguments to json file
    config_json_path = project_loc + "/config.json"
    with open(config_json_path, "w") as file:
        json.dump(args, file, indent=4)
    print("\tSaved ", config_json_path)

    return args, config_json_path
