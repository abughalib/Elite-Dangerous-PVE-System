import argparse

all_args = argparse.ArgumentParser(description="PVE System")

all_args.add_argument("-r", "--ref", required=False, help="Reference System", default="SOL")

all_args.add_argument("-d", "--dist", required=False,
                      help="Distance From Reference System example finding system within 20Ly i.e --dist 20",
                      default=20)
all_args.add_argument("-f", "--fed", required=False,
                      help="Minimum No of Federation Factions", default=0)
all_args.add_argument("-e", "--imp", required=False,
                      help="Minimum No of Imperial Factions", default=0)
all_args.add_argument("-a", "--all", required=False,
                      help="Minimum No of Alliance Factions", default=0)
all_args.add_argument("-i", "--ind", required=False,
                      help="Minimum No of Independent Factions", default=0)
all_args.add_argument("-s", "--res", required=False,
                      help="Bounty Hunting Site: any, CNB, low, high, reg, haz", default="any")