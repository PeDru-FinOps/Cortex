#cloud8 #azure #finops #governance #cloudcomputing 

A pausa de capacidade do Fabric é uma boa prática para otimização de custos, evitando o recebimento de cobranças pelos periodos onde a capacidade não é utilizada. Microsoft Fabric permite pausar e retomar sua capacidade. Quando sua capacidade não estiver operacional, você poderá pausar para habilitar a economia de custos para sua organização. Posteriormente, quando você quiser retomar o trabalho em sua capacidade, poderá reativar isso.
## Pré-Requisitos

Para pausar sua capacidade, você precisa:

- Uma [capacidade F SKU](https://learn.microsoft.com/pt-br/fabric/enterprise/buy-subscription#azure-skus)
- As seguintes ações de RBAC do Azure no recurso de capacidade do Fabric:
    
    - `Microsoft.Fabric/capacities/read`
    - `Microsoft.Fabric/capacities/write`
    - `Microsoft.Fabric/capacities/suspend/action`
    - `Microsoft.Fabric/capacities/resume/action`
    
Crie uma função personalizada [Azure](https://learn.microsoft.com/pt-br/azure/role-based-access-control/custom-roles) com escopo para essas ações. Essas ações também são incluídas nas [funções integradas privilegiadas do Azure](https://learn.microsoft.com/pt-br/azure/role-based-access-control/built-in-roles/privileged), mas não se recomenda o uso dessas funções, pois elas concedem mais permissões do que o necessário.
## Start/Stop da capacidade através do Portal Azure

1. Entre no [portal do Azure](https://portal.azure.com/);
2. Em Serviços do Azure, selecione Microsoft Fabric;
3. Selecione a capacidade que deseja pausar, para visualizar os detalhes. Em seguida clique em Pausar, e confirme clicando em Sim.

Para iniciar novamente a capacidade do Power BI Embedded basta seguir o mesmo procedimento, clicando em Start e confirmando.
## Start/Stop da capacidade através do Azure CLI

Para realizar o Start/Stop de uma capacidade do Power BI Embedded através de automação, será necessário utilizar o Módulo Az.PowerBiEmbedded. A automação pode ser configurada através de Resource ID ou a combinação de Resource Group Name + Resource Name.

### Stop

#### CLI

`` az fabric capacity suspend --resource-group TestRG --capacity-name azsdktest

#### Powershell

````
Suspend-AzFabricCapacity
    -CapacityName <String>
    -ResourceGroupName <String>
    [-SubscriptionId <String>]
    [-DefaultProfile <PSObject>]
    [-AsJob]
    [-NoWait]
    [-PassThru]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]
    
# Exemplo

Suspend-AzFabricCapacity -ResourceGroupName "testrg" -CapacityName "azsdktest"
````
#### Automação

````
Connect-AzAccount -Identity  
# Ativar Managed Identity na Automation Account  
# Conceder permissões via RBAC nos recursos ou subscriptions necessárias  
  
Set-AzContext -Subscription <subscription_id>  
  
try  
{  
Suspend-AzFabricCapacity -ResourceGroupName "testrg" -CapacityName "azsdktest" -PassThru  
  
Write-Output "Fabric Capacity Successfully Stopped"  
}  
catch  
{  
Write-Error -Message $_.Exception  
throw  $_.Exception  
}
````
### Start

#### CLI

`` az fabric capacity resume --resource-group TestRG --capacity-name azsdktest

#### Powershell

````
Resume-AzFabricCapacity
    -CapacityName <String>
    -ResourceGroupName <String>
    [-SubscriptionId <String>]
    [-DefaultProfile <PSObject>]
    [-AsJob]
    [-NoWait]
    [-PassThru]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

# Exemplo

Resume-AzFabricCapacity -ResourceGroupName "testrg" -CapacityName "azsdktest"
````

#### Automação

````
Connect-AzAccount -Identity  
# Ativar Managed Identity na Automation Account  
# Conceder permissões via RBAC nos recursos ou subscriptions necessárias  
  
Set-AzContext -Subscription <subscription_id>  
  
try  
{  
Resume-AzFabricCapacity -ResourceGroupName "testrg" -CapacityName "azsdktest"
  
Write-Output "Fabric Capacity Successfully Resumed"  
}  
catch  
{  
Write-Error -Message $_.Exception  
throw  $_.Exception  
}
````
## Referências

https://learn.microsoft.com/pt-br/fabric/enterprise/pause-resume
### Powershell

https://learn.microsoft.com/pt-br/powershell/module/az.fabric/suspend-azfabriccapacity?view=azps-15.6.0

https://learn.microsoft.com/pt-br/powershell/module/az.fabric/resume-azfabriccapacity?view=azps-15.6.0
### CLI

https://learn.microsoft.com/pt-br/rest/api/microsoftfabric/fabric-capacities/resume?view=rest-microsoftfabric-2023-11-01&tabs=HTTP

https://community.fabric.microsoft.com/t5/Fabric-platform/How-to-Pause-Resume-a-Fabric-Capacity-on-the-command-line/m-p/4640379
### APIs

https://learn.microsoft.com/pt-br/rest/api/microsoftfabric/fabric-capacities/suspend?view=rest-microsoftfabric-2023-11-01&tabs=HTTP

https://learn.microsoft.com/pt-br/rest/api/microsoftfabric/fabric-capacities/resume?view=rest-microsoftfabric-2023-11-01&tabs=HTTP
  
  