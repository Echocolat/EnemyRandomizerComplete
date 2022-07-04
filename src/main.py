from enemizer import Enemizer
from enemizer_config import EnemizerConfig

WELCOME = str(
    "    /\\                          /\\\n"
    + "   /__\\     Welcome to the     /__\\\n"
    + "  /\\  /\\   BotW Ene-mizer!    /\\  /\\\n"
    + " /__\\/__\\                    /__\\/__\\\n"
    + "\n"
    + "Customize settings (y/N) "
)


def main():

    opt: EnemizerConfig = EnemizerConfig()

    # Assign options
    if input(WELCOME) == "y":

        print(
            "Enter 'y' or 'n' for the following options:\n\n"
            + "\tRandomize enemies in..."
        )

        # Assign randomized locations
        opt.main_field = input("\t\tOverworld (Y/n) ").lower() != "n"
        opt.shrines = input("\t\tShrines (Y/n) ").lower() != "n"
        opt.divine_beasts = input("\t\tDivine Beasts (Y/n) ").lower() != "n"
        opt.aoc_field = input("\t\tThe Trial of the Sword (Y/n) ").lower() != "n"

        # Assign misc options
        opt.chaos = (
            input(
                "\n\tChaos Mode: All enemies have an equal chance of spawning (NOT RECOMMENDED)\n"
                + "\t\tActivate Chaos mode? (y/N) "
            ).lower()
            == "y"
        )

        if not opt.chaos:

            _boss_prob = input(
                "\n\tChoose the spawn probability of mini-bosses.\n"
                + "\t\tEnter a number from 1-100 (leave empty for the default value): "
            )

            while (type(_boss_prob) is not int) or _boss_prob != "":
                _boss_prob = input(
                    f"{_boss_prob} is not a valid number. Please enter a number: "
                )

            opt.boss_prob = int(_boss_prob) if _boss_prob != "" else 23

    Enemizer(opt).randomize()


if __name__ == "__main__":
    main()
