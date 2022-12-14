
def start_app(config: dict) -> bool:
    print(f'Start application with config:')
    for k, v in config.items():
        print(f'\t{k}={v}')
    return True