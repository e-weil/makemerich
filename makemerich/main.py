"""
MakeMeRich — The AI that actually makes you money.
Main entry point.
"""

import asyncio
import argparse

from makemerich.core.engine import Engine


def main():
    parser = argparse.ArgumentParser(description="MakeMeRich Trading Agent")
    parser.add_argument("--config", default="config/default.yaml",
                       help="Path to config file")
    parser.add_argument("--mode", choices=["paper", "live"], default="paper",
                       help="Trading mode (default: paper)")
    parser.add_argument("--pairs", nargs="+", default=["BTCUSDT"],
                       help="Trading pairs")
    args = parser.parse_args()

    engine = Engine(config_path=args.config)

    if args.mode:
        engine.config.mode = args.mode
    if args.pairs:
        engine.config.trading_pairs = args.pairs

    print("""
    ╔═══════════════════════════════════════╗
    ║         MakeMeRich                    ║
    ║   The AI that actually makes you $    ║
    ║                                       ║
    ║   Mode: {mode:<30s}║
    ║   Pairs: {pairs:<29s}║
    ╚═══════════════════════════════════════╝
    """.format(mode=args.mode, pairs=", ".join(args.pairs)))

    asyncio.run(engine.start())


if __name__ == "__main__":
    main()
