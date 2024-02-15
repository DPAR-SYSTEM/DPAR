import json
import yaml
import logging
import logging.handlers
from .UI import mainUI
from .recommender import Recommender_module_v1 as Recommender_module
from .recommender import suggestions_optimizer
from .model import PESrank
import os
path = os.getcwd()

log = logging.getLogger()


def init_logging():
    """Initialize logger."""
    logging.basicConfig(filename='model.log', level=logging.DEBUG,
                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")


init_logging()

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
ymlz = os.path.join('config.yaml')


def main(username, password):
    with open(ymlz) as file:
        conf = yaml.safe_load(file)

    ### Fetching model's results
    model = PESrank.PESrank(password)
    model_results = model.main_pesrank()
    model_results['username'] = username

    ### Fetching recommendations
    recomm = Recommender_module.Recommendor(model_results, path)

    recommensations = recomm.recommender_main()

    ### Applying optimization
    opts = suggestions_optimizer.Optimized(recommensations)

    optimzed_results_1 = opts.max_list()

    optimzed_results_2 = {}
    for index, value in optimzed_results_1.items():
        if value[0] == '':
            # print(value[0])
            optimzed_results_2[index] = (value[0], 0)
        else:
            # print(value[0])
            mod1 = PESrank.PESrank(value[0])
            adjusted_bits = mod1.main_pesrank()['bits']
            optimzed_results_2[index] = (value[0], adjusted_bits)

    # print(optimzed_results_2)
    # model = PESrank.PESrank(password, path)
    model_results['1'] = optimzed_results_2['1']
    model_results['2'] = optimzed_results_2['2']
    model_results['3'] = optimzed_results_2['3']
    model_results['4'] = optimzed_results_2['4']
    model_results['5'] = optimzed_results_2['5']
    model_results['6'] = optimzed_results_2['6']
    model_results['7'] = optimzed_results_2['7']

    ui_results = mainUI.main(model_results)
    # print(json.dumps(ui_results, indent=4))
    print(json.dumps(model_results, indent=4))
    return ui_results, model_results



