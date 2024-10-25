import argparse
from engine.news_engine.bilibili import bilibili

def run(dry_run=False):
    results = bilibili(dry_run=dry_run)
    if dry_run:
        print(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the news engine.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run which print the result and prevent writing to the database.')
    args = parser.parse_args()
    
    run(dry_run=args.dry_run)