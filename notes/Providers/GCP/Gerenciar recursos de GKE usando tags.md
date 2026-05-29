#gcp #finops #cloudcomputing 

As [[Tags]] são pares de chave-valor que permitem anotar e gerenciar seus Google Cloud recursos no nível da organização ou do projeto. Use tags para organizar seus recursos e aplicar condicionalmente políticas, como firewalls ou políticas do IAM. Elas oferecem suporte ao controle de acesso do IAM, que permite definir quem pode anexar, criar, atualizar ou excluir tags.
## Caso de uso de tags no GKE

Use tags no GKE em situações como as seguintes:

- Aplique condicionalmente políticas de firewall de rede a nós específicos. Por exemplo, negue o tráfego de entrada da Internet pública para todos os nós de um cluster em ambientes de preparo ou teste. Para instruções, consulte [Aplicar seletivamente políticas de firewall de rede no GKE](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/tags-firewall-policies?hl=pt-br).
- Conceda condicionalmente papéis do IAM com base em tags. Por exemplo, conceder automaticamente aos contratados acesso a ambientes específicos que normalmente estariam disponíveis apenas para funcionários em tempo integral. Para ver instruções, consulte o restante deste documento.
- Audite e analise as informações de faturamento com base nas tags aplicadas no nível do projeto ou da organização.

## Requisitos

- Ativar a API Google Kubernetes Engine.
- Verifique se você tem os seguintes papéis do IAM:
	- `roles/resourcemanager.tagAdmin`
	- `roles/resourcemanager.tagUser`

## ResourceID de Cluster Kubernetes
`//container.googleapis.com/projects/PROJECT_ID/locations/CLUSTER_LOCATION/clusters/CLUSTER_NAME`.

## Rótulo de Node, de Nodepool e de Kubernetes

Os rótulos de cluster do GKE e do nodepool são diferentes dos [rótulos do Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). Os dois sistemas de rotulagem funcionam de forma independente e não herdam nem compartilham rótulos.

Os rótulos de cluster do GKE e do nodepool são metadados arbitrários anexados aos recursos. Você pode usar esses rótulos para acompanhar informações sobre faturamento e uso.

Separadamente, no Kubernetes, o sistema usa rótulos internamente para associar componentes e recursos do cluster (por exemplo, pods e nós) entre si e gerenciar ciclos de vida de recursos. É possível editar os rótulos do Kubernetes com a API Kubernetes. 

Também é possível usar a API GKE para editar rótulos do Kubernetes nos nodes com a [criação de cluster](https://docs.cloud.google.com/sdk/gcloud/reference/container/node-pools/create?hl=pt-br#--node-labels) ou com uma [atualização de cluster](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/update-existing-nodepools?hl=pt-br#updating_node_labels). Para mais informações, consulte [Atualizar rótulos e taints de nós do Kubernetes para pools de nós](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/update-existing-nodepools?hl=pt-br).

- Um rótulo de cluster é um par de chave-valor que pode ser atribuído a clusters do Google Cloud.

## Rótulos aplicados automaticamente

O GKE aplica automaticamente vários identificadores aos recursos de cluster.

Por exemplo, o GKE aplica rótulos a instâncias do Compute Engine, discos permanentes e aceleradores (TPU).

A tabela a seguir lista os identificadores que o GKE aplica automaticamente aos recursos:

| Rótulo                                  | Recursos aplicados                                                                                                                                             |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `goog-gke-node`                         | Instância de VM do Compute Engine subjacente a um nó do GKE.                                                                                                   |
| `goog-gke-volume`                       | Disco permanente do Compute Engine anexado a uma instância de VM subjacente a um nó do GKE.                                                                    |
| `goog-gke-tpu`                          | [Cloud TPU no GKE](https://docs.cloud.google.com/tpu/docs/kubernetes-engine-setup?hl=pt-br).                                                                   |
| `goog-k8s-cluster-name`                 | Instância de VM do Compute Engine e discos permanentes anexados a uma instância de VM subjacente a um nó do GKE.                                               |
| `goog-k8s-cluster-location`             | Instância de VM do Compute Engine e discos permanentes anexados a uma instância de VM subjacente a um nó do GKE.                                               |
| `goog-k8s-node-pool-name`               | Instâncias de VM do Compute Engine e os discos de inicialização subjacentes a um nó do GKE.                                                                    |
| `goog-fleet-project`                    | Instância de VM do Compute Engine e discos permanentes anexados a uma instância de VM subjacente a um nó do GKE, se o cluster estiver registrado em uma frota. |
| `goog-gke-accelerator-type`             | Pool de nós do GKE.                                                                                                                                            |
| `goog-gke-tpu-node-pool-type`           | Pool de nós do GKE.                                                                                                                                            |
| `goog-gke-node-pool-provisioning-model` | Pool de nós do GKE.                                                                                                                                            |

Não edite ou exclua rótulos reservados. Todas as mudanças feitas nos rótulos reservados são reconciliadas automaticamente.

## Referência

https://docs.cloud.google.com/kubernetes-engine/docs/how-to/tags?hl=pt-br
https://docs.cloud.google.com/kubernetes-engine/docs/how-to/creating-managing-labels?hl=pt-br

