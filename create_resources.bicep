param storageAccountName string
param appServiceName string

// Azure Blob Storageを作成する
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: storageAccountName
  location: resourceGroup().location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
  }
}

// Azure App Serviceを作成する
resource appServicePlan 'Microsoft.Web/serverfarms@2021-01-15' = {
  name: appServiceName
  location: resourceGroup().location
  sku: {
    name: 'B1'
    tier: 'Basic'
    size: 'B1'
    capacity: 1
  }
  properties: {
    reserved: true // Linux環境に変更
  }
}

resource appService 'Microsoft.Web/sites@2021-01-15' = {
  name: appServiceName
  location: resourceGroup().location
  kind: 'app'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
    }
  }
}
