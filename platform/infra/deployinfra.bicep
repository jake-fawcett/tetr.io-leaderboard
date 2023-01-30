@description('This is the resource location')
param location string = resourceGroup().location

@description('This is the Storage Account name')
param storageAccountName string

@description('This is the Storage Account sku')
param storageAccountSku string

@description('This is the Storage Account tier')
param storageAccountTier string

@description('This is the Web App Server name')
param webAppServerName string

@description('This is the Web App Server kind')
param webAppServerKind string

@description('This is the Web App Server sku')
param webAppServerSku string

@description('This is the Web App Server capacity')
param webAppServerSkuCapacity int

@description('This is the Web App name')
param webAppName string

@description('This is the Web App Software version')
param webAppLinuxFxVersion string

resource storageAccount 'Microsoft.Storage/storageAccounts@2019-06-01' = {
  name: storageAccountName
  location: location
  properties: {
    accessTier: storageAccountTier
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      bypass: 'Logging, Metrics, AzureServices'
      defaultAction: 'Deny'
      ipRules: []
      virtualNetworkRules: []
    }
  }
  sku: {
    name: storageAccountSku
  }
  kind: 'StorageV2'
}

resource webAppServer 'Microsoft.Web/serverfarms@2020-06-01' = {
  name: webAppServerName
  location: location
  kind: webAppServerKind
  properties: {
  }
  sku: {
    name: webAppServerSku
    capacity: webAppServerSkuCapacity
  }
}

resource webApp 'Microsoft.Web/sites@2020-06-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: webAppServer.id
    siteConfig: {
      linuxFxVersion: webAppLinuxFxVersion
    }
  }
}

output serverFarmID string = webAppServer.id
output webAppID string = webApp.id
output storageID string = storageAccount.id
