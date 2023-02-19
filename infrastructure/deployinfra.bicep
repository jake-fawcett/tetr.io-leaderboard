@description('This is the resource location')
param location string = resourceGroup().location

@description('This is the Storage Account name')
param storageAccountName string

@description('This is the Storage Account sku')
param storageAccountSku string = 'Standard_LRS'

@description('This is the Storage Account tier')
param storageAccountTier string = 'Hot'

@description('This is the Web App Server name')
param webAppServerName string

@description('This is the Web App Server kind')
param webAppServerKind string

@description('This is the Web App Server sku')
param webAppServerSku string

@description('This is the Web App name')
param webAppName string

@description('This is the Web App Software version')
param webAppLinuxFxVersion string

module storageAccount 'bicep-modules/storage/storageAccount.bicep' = {
  name: 'storageAccountDeploy'
  params: {
    location: location
    storageAccountName: storageAccountName
    storageAccountSku: storageAccountSku
    storageAccountTier: storageAccountTier
    storageAccountPublicAccess: 'Enabled' // To be removed when private networking implemented
    storageAccountDefaultNetworkAcl: 'Allow' // To be removed when private networking implemented
  }
}

module storageAccountTableService 'bicep-modules/storage/tableService.bicep' = {
  name: 'tableServiceDeploy'
  dependsOn: [
    storageAccount
  ]
  params: {
    storageAccountName: storageAccountName
  }
}

module usersTable 'bicep-modules/storage/table.bicep' = {
  name: 'tableDeploy'
  dependsOn: [
    storageAccountTableService
  ]
  params: {
    storageAccountName: storageAccountName
    tableName: 'users'
  }
}

module webappServer 'bicep-modules/webapp/serverFarm.bicep' = {
  name: 'serverFarmDeploy'
  params: {
    location: location
    webAppServerName: webAppServerName
    webAppServerKind: webAppServerKind
    webAppServerSku: webAppServerSku
  }
}

module webapp 'bicep-modules/webapp/site.bicep' = {
  name: 'webappDeploy'
  dependsOn: [
    webappServer
  ]
  params: {
    location: location
    webAppServerName: webAppServerName
    webAppName: webAppName
    webAppLinuxFxVersion: webAppLinuxFxVersion
    webAppPublicNetworkAccess: 'Enabled'
  }
}
