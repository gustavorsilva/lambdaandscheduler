import boto3
import fnmatch
import sys
import os

def perform_scaling_action(pattern, desired, min_size, max_size):
    # Inicializar o cliente do serviço Auto Scaling
    autoscaling_client = boto3.client('autoscaling')

    # Filtrar os grupos de Auto Scaling com base no padrão especificado
    grupos_correspondentes = fnmatch.filter(get_all_auto_scaling_groups(), pattern)

    # Realizar a ação (start ou stop) para os grupos de Auto Scaling correspondentes
    if action == 'start' or action == 'stop':
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
    # Inicializar o cliente do serviço Auto Scaling
    autoscaling_client = boto3.client('autoscaling')

    # Obter a lista de todos os grupos de Auto Scaling
    response = autoscaling_client.describe_auto_scaling_groups()
    grupos_auto_scaling = response['AutoScalingGroups']
    return [grupo['AutoScalingGroupName'] for grupo in grupos_auto_scaling]

# Exemplo de uso do script Python
if __name__ == "__main__":

    action = os.environ.get('ACTION')

    if action not in ['start', 'stop']:
        sys.exit(1)

    if action == 'start':
        perform_scaling_action('testela*', 1, 1, 2)
    elif action == 'stop':
        perform_scaling_action('testelam*', 0, 0, 0)
    
    # Retornar uma mensagem de conclusão
    print(f"Alterações de scaling realizadas com sucesso para a ação '{action}'")
