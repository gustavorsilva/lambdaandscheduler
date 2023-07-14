import boto3

def lambda_handler(event, context):
    autoscaling_client = boto3.client('autoscaling')

    grupos = [
        {'nome': 'testelambda', 'desired_cap':0, 'min_node':0, 'max_node':0}
    ]

    # Alterando grupo do auto scaling
    for grupo in grupos:
        response = autoscaling_client.update_auto_scaling_group(
            AutoScalingGroupName=grupo['nome'],
			DesiredCapacity=grupo['desired_cap'],
			MinSize=grupo['min_node'],
			MaxSize=grupo['max_node']
        )
        print(f"Grupo {grupo['nome']} atualizado com sucesso. Nova quantidade: {grupo['desired_cap'], grupo['min_node'], grupo['max_node']}")

    return "Alterações de scaling realizadas com sucesso"
