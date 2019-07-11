versions = {
    "0.4.1": 'first_version',
    "0.6.1": {
        'Move': [
            {
                'Way': 'gui/sensors/0/range_axis_y',
                'To': 'gui/sensors/0/range_axis_y/max'
                },
            {
                'Way': 'gui/sensors/0/range_axis_x',
                'To': 'gui/sensors/0/range_axis_x/max'
                },
            {
                'Way': 'gui/sensors/1/range_axis_y',
                'To': 'gui/sensors/1/range_axis_y/max'
                },
            {
                'Way': 'gui/sensors/1/range_axis_x',
                'To': 'gui/sensors/1/range_axis_x/max'
                }
            ],
        'Add': [
            {
                'Way': 'gui/snapshot_maker',
                'Data': [0, 0]
                },
            {
                'Way': 'gui/wlm_data_export',
                'Data': [0, 0] 
                },
            {
                'Way': 'gui/sensors/0/range_axis_y/min',
                'Data': 0
                },
            {
                'Way': 'gui/sensors/1/range_axis_y/min',
                'Data': 0
                },
            {
                'Way': 'gui/sensors/1/range_axis_x/min',
                'Data': 1
                },
            {
                'Way': 'gui/sensors/0/range_axis_x/min',
                'Data': 1
                }
            ]
        },
    "0.7.2": {
        'Move': [
            {
                'Way': 'hwsc/src',
                'To': 'gui/helecopter'
                },
            {
                'Way': 'hwsc/hwsc_presets/broadcast_port',
                'Rename': 'jesus_crazy'
                }
            ],
        'Add': [
            {
                'Way': 'logo',
                'Data': ''
                }
            ]
        }
    }
