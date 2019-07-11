versions = {
    "1.0": 'first_version',
    "1.1": {
        'Add': [
            {
                'Way': 'serial_number',
                'Data': 2000
                },
            {
                'Way': 'sensors/description/sensor_id',
                'Data': "1"
                },
            {
                'Way': 'sensors/description/name',
                'Data': "WS-415"
                },
            {
                'Way': 'sensors/modes',
                'Data': "standart"
                },
            {
                'Way': 'sensors/modes',
                'Data': "extended"
                },
            {
                'Way': 'sensors/basic_settings/GAIN',
                'Data': 40
                },
            {
                'Way': 'sensors/basic_settings/INTEGRATION_TIME',
                'Data': 24
                },
            {
                'Way': 'sensors/duration',
                'Data': 361
                },
            {
                'Way': 'sensors/basic_settings/sensor_id',
                'Data': "1"
                }
            ]
        },
    "1.3": {
        'Add': [
            {
                'Way': 'sensors/description',
                'Data': {"sensor_id": 2, "name": "WS-420"}
                },
            {
                'Way': 'sensors/description',
                'Data': {"sensor_id": 3, "name": "WS-423"}
                },
            {
                'Way': 'connection_port',
                'Data': 7
                },
            {
                'Way': 'src',
                'Data': "./hwsc.dll"
                }
            ],
        'Move': [
            {
                'Way': 'sensors/basic_settings',
                'To': 'basic_settings'
                },
            {
                'Way': 'sensors/duration',
                'Rename': 'exit_time'
                }
            ]
        },
    "2.1": {
        'Add': [
            {
                'Way': 'sensors/modes',
                'Data': "developer"
                }
            ],
        'Move': [
            {
                'Way': 'src',
                'Rename': 'adress'
                }
            ],
        'Delete': [
            {
                'Way': 'connection_port'
                },
            ]
        }
    }