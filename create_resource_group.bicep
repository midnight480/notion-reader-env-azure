// dotenvから変数を読み込む
param resourceGroupName string = '${env:RESOURCE_GROUP_NAME}'

// リソースグループを作成する
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
}
