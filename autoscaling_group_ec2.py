import boto3
import fnmatch

def lambda_handler(event, context):
    autoscaling_client = boto3.client('autoscaling')

    scaling_groups = {
        'teste*': {
            'desired_cap': 0,
            'min_node': 0,
            'max_node': 0
        }
    }

    response = autoscaling_client.describe_auto_scaling_groups()
    grupos_scaling = response['AutoScalingGroups']

    for grupo in grupos_scaling:
        name_scaling_node = grupo['AutoScalingGroupName']
        for scaling_name, valores in scaling_groups.items():
            if fnmatch.fnmatch(name_scaling_node, scaling_name + '*'):
                try:
                    response = autoscaling_client.update_auto_scaling_group(
                        AutoScalingGroupName=name_scaling_node,
                        DesiredCapacity=valores['desired_cap'],
                        MinSize=valores['min_node'],
                        MaxSize=valores['max_node']
                    )
                    print(f"Grupo {name_scaling_node} atualizado com sucesso.")
                except Exception as e:
                    print("Fail")
