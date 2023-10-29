from scheduling_optimization import get_schedule 


def model(suc_code, demanda, trabajadores):
    results_dict, loss = get_schedule(demanda, trabajadores)

    return loss
    


if __name__ == "__main__":
    import json

    def load_json(path):
        with open(path, 'r') as f: 
            data = json.load(f)
        return data 


    l = []
    for b in [60,311,487,569,834]:
        demanda_path = f"/home/juan/dev/dataton2023-optilab/test/data/input/demanda_{b}.json"
        trabajadores_path = f"/home/juan/dev/dataton2023-optilab/test/data/input/trabajadores_{b}.json"

        demanda = load_json(demanda_path)
        trabajadores = load_json(trabajadores_path)

        l.append(model(60, demanda, trabajadores))

    print(l, sum(l))
