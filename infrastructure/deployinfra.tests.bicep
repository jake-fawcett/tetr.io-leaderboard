module test_required_params 'deployinfra.bicep' = {
  name: 'test_required_params'
  params: {
    environment: 'Test'
    storageAccountName: 'stracttest'
    storageAccountSku: 'Standard_LRS'
    storageAccountTier: 'Hot'
    webAppServerName: 'platform-tetris-webapp-server-test'
    webAppServerKind: 'linux'
    webAppServerTier: 'Basic'
    webAppServerSku: 'B1'
    webAppServerSkuCapacity: 1
    webAppName: 'platform-tetris-webapp-test'
    webAppLinuxFxVersion: '"PYTHON|3.9"'
  }
}
