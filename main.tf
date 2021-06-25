terraform { 
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm" 
            version = ">= 2.49"
        }
    }
} 
provider "azurerm" { 
    features {}
} 
data "azurerm_resource_group" "main" { 
    name = "AmericanExpress1_JasonBuckenham_ProjectExercise"
}