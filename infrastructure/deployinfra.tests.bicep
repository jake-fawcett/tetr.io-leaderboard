module test_required_params 'deployinfra.bicep' = {
  name: 'test_required_params'
  params: {
    location: 'UkSouth'
    tags: {"environment": "TEST"}
    storageAccountName: 'stracttest'
    webAppServerName: 'platform-tetris-webapp-server-test'
    webAppServerKind: 'linux'
    webAppServerSku: 'B1'
    webAppName: 'platform-tetris-webapp-test'
    webAppLinuxFxVersion: '"PYTHON|3.9"'
  }
}
