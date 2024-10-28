import db


def main():

    ambientes = db.get_ambientes()
    if ambientes is None:
        print("Deu pau")
        exit(1)
    print("Ambientes: ")
    print()
    for ambiente in ambientes:
        print(f"{ambiente.nome}")
        print(f"Temperatura Desejada: {ambiente.temperaturaDesejada} °C")
        print(f"Localização: {ambiente.cidade}")
        if not ambiente.ares_condicionados:
            continue
        for ar in ambiente.ares_condicionados:
            print(f"    Ar-condicionado #{ambiente.ares_condicionados.index(ar)+1}")
            print(f"        Nome: {ar.nome}")
            print(f"        Marca: {ar.marca}")
            print(f"        Capacidade: {ar.capacidade_total}")
        print("_________________________________________________________")


if __name__ == "__main__":
    main()

