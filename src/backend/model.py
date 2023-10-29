from scheduling_optimization import get_schedule 


def model(suc_code, demanda, trabajadores):
    results_dict = get_schedule(demanda, trabajadores)
    


if __name__ == "__main__":
    import json

    def load_json(path):
        with open(path, 'r') as f: 
            data = json.load(f)
        return data 

    demanda_path = "/home/juan/dev/dataton2023-optilab/test/data/input/demanda_60.json"
    trabajadores_path = "/home/juan/dev/dataton2023-optilab/test/data/input/trabajadores_60.json"

    demanda = load_json(demanda_path)
    trabajadores = load_json(trabajadores_path)

    model(60, demanda, trabajadores)


