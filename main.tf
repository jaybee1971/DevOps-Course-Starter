terraform {
  backend "azurerm" {
    resource_group_name = "AmericanExpress1_JasonBuckenham_ProjectExercise"
    storage_account_name = "jbtodoappstorage"
    container_name = "jb-todoapp-container"
    key = "https://jbtodokeyvault.vault.azure.net/secrets/jb-back-end-key/043c37b759244682b42a76f17957df3a"
  }
}
 
provider "azurerm" { 
    features {}
} 
data "azurerm_resource_group" "main" { 
    name = "AmericanExpress1_JasonBuckenham_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
    name = "terraformed-asp"
    location = var.location
    resource_group_name = data.azurerm_resource_group.main.name
    kind = "Linux"
    reserved = true

    sku {
        tier = "Basic"
    size = "B1"
    }
} 

resource "azurerm_cosmosdb_account" "main" {
    name = "${var.prefix}-cosmosdb-account"
    resource_group_name = data.azurerm_resource_group.main.name
    location = var.location
    offer_type = "Standard"
    kind = "MongoDB"
    capabilities {
        name = "EnableServerless"
    }
    capabilities {
        name = "EnableMongo"
    }
    consistency_policy {
        consistency_level = "BoundedStaleness"
        max_interval_in_seconds = 10
        max_staleness_prefix = 200
    }
    geo_location {
        location = data.azurerm_resource_group.main.location
        failover_priority = 0
    }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
    name = "${var.prefix}-todoapp-db"
    resource_group_name = data.azurerm_resource_group.main.name
    account_name = azurerm_cosmosdb_account.main.name
    #lifecycle { prevent_destroy = true }
}

resource "azurerm_app_service" "main" {
    name = "${var.prefix}-terraform-todo-app"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id

    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|jaybee1971/todo_app:latest"
    } 
    app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
        "MONGO_URL" = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
        "MONGO_DB" = "${var.prefix}-todoapp-db"
        "FLASK_APP" = "todo_app.app"
        "FLASK_ENV" = "production"
        "SECRET_KEY" = "jbtodoapp"
        "GH_CLIENT_ID" = var.GH_CLIENT_ID
        "GH_SECRET" = var.GH_SECRET
    }
}
