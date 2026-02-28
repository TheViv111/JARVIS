import sounddevice as sd

print('Available audio devices:')
for i, device in enumerate(sd.query_devices()):
    print(f'  {i}: {device["name"]}')
    print(f'      Input channels: {device["max_input_channels"]}')
    print(f'      Output channels: {device["max_output_channels"]}')
    print(f'      Default sample rate: {device["default_samplerate"]}')
    print()
