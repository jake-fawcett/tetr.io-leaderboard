@description('This is the resource location')
param location string = resourceGroup().location

@description('This is the resource location')
param environment string

@description('This is the resource location')
param tags object  = {environment: environment}

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
param webAppServerTier string = 'Basic'

@description('This is the Web App Server sku')
param webAppServerSku string

@description('This is the Web App Server capacity')
param webAppServerSkuCapacity int = 1

@description('This is the Web App name')
param webAppName string

@description('This is the Web App Software version')
param webAppLinuxFxVersion string

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' = {
  name: storageAccountName
  location: location
  tags: tags
  properties: {
    accessTier: storageAccountTier
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      bypass: 'Logging, Metrics, AzureServices'
      defaultAction: 'Deny'
    }
  }
  sku: {
    name: storageAccountSku
  }
  kind: 'StorageV2'
}

resource symbolicname 'Microsoft.Storage/storageAccounts/blobServices@2022-05-01' = {
  name: 'default'
  parent: storageAccount
  properties: {
    containerDeleteRetentionPolicy: {
      allowPermanentDelete: true
      days: 7
      enabled: true
    }
    deleteRetentionPolicy: {
      allowPermanentDelete: true
      days: 7
      enabled: true
    }
    isVersioningEnabled: true
  }
}

resource storageAccountTableService 'Microsoft.Storage/storageAccounts/tableServices@2022-05-01' = {
  name: 'default'
  parent: storageAccount
  properties: {}
}

resource usersTable 'Microsoft.Storage/storageAccounts/tableServices/tables@2022-05-01' = {
  name: 'users'
  parent: storageAccountTableService
  properties: {}
}

resource webAppServer 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: webAppServerName
  location: location
  tags: tags
  kind: webAppServerKind
  properties: {
    reserved: true
  }
  sku: {
    name: webAppServerSku
    tier: webAppServerTier
    capacity: webAppServerSkuCapacity
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  tags: tags
  properties: {
    serverFarmId: webAppServer.id
    clientAffinityEnabled: false
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: webAppLinuxFxVersion
      minTlsVersion: '1.2'
      http20Enabled: true
      ftpsState: 'FtpsOnly'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'True'
        }
      ]
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}
