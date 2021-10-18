import os

project_loc = os.getcwd()
input = "/inputs"
output = "/outputs"
countries_file = "/countries.gpkg"

with open(".env", "w") as f:
    f.write(f"DATA_PATH='{project_loc}'\n")
    f.write(f"INPUT_PATH='{project_loc}{input}'\n")
    f.write(f"OUTPUT_PATH='/share/rkmeente/cawalden/pops_global{output}'\n")
    f.write(f"COUNTRIES_PATH='{project_loc}{input}{countries_file}'\n")
    f.close()
