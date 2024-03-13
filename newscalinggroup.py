import boto3
import fnmatch
import os

def perform_scaling_action(pattern, desired, min_size, max_size):
    autoscaling_client = boto3.client('autoscaling')

    # Filtrar os grupos de Auto Scaling
    grupos_correspondentes = fnmatch.filter(get_all_auto_scaling_groups(), pattern)

    # Realizar a ação (start ou stop) para os grupos de Auto Scaling correspondentes
    for grupo_correspondente in grupos_correspondentes:
        try:
            response = autoscaling_client.update_auto_scaling_group(
                AutoScalingGroupName=grupo_correspondente,
                DesiredCapacity=desired,
                MinSize=min_size,
                MaxSize=max_size
            )
            print(f"Grupo {grupo_correspondente} atualizado com sucesso.")
            print(f"Novo DesiredCapacity: {desired}")
            print(f"Novo MinSize: {min_size}")
            print(f"Novo MaxSize: {max_size}")
        except Exception as e:
            print(f"Erro ao atualizar o grupo {grupo_correspondente}: {str(e)}")

def get_all_auto_scaling_groups():
    autoscaling_client = boto3.client('autoscaling')

    # lista de todos os grupos de Auto Scaling
    response = autoscaling_client.describe_auto_scaling_groups()
    grupos_auto_scaling = response['AutoScalingGroups']
    return [grupo['AutoScalingGroupName'] for grupo in grupos_auto_scaling]

def lambda_handler(event, context):
    action = event.get('action')
    desired = event.get('desired', 0)
    min_size = event.get('min_size', 0)
    max_size = event.get('max_size', 0)

    if action not in ['start', 'stop']:
        return {
            'statusCode': 400,
            'body': 'Ação inválida. As opções válidas são "start" e "stop".'
        }

    # start ou stop via action
    if action == 'start':
        perform_scaling_action('eks-node*', 1, 1, 1)
    elif action == 'stop':
        perform_scaling_action('eks-node*', 0, 0, 0)

    # Status de Atividade
    return {
        'statusCode': 200,
        'body': f'Alterações de scaling realizadas com sucesso para a ação "{action}".'
    }


###### teste json ######
#{
#  "action": "start" ou "action": "stop"
#}
