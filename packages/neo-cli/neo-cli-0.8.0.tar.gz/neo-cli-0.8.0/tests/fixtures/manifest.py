fake_manifest = {
    "deploy_dir": "/path/to/.deploy",
    "stack": {
        "services": [],
        "networks": [],
        "deployments": [],
        "clusters": [],
        "instances": ["awesome-project"],
        "databases": [],
        "others": [],
    },
    "data": {
        "deploy": ["instances.awesome-project"],
        "instances": {
            "awesome-project": {
                "parameters": {
                    "flavor": "SX48.8",
                    "image": "CentOS 6.9",
                    "key_name": "vm-key",
                    "private_network": "vm-net",
                    "username": "john",
                },
                "template": "vm",
            }
        },
    },
}
