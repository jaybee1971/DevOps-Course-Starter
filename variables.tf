variable "prefix" {
    description = "The prefix used for all resources in this environment"
}

variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default = "uksouth"
}

variable "GH_CLIENT_ID" {
 description = "The Github client Id env variable"
}

variable "GH_SECRET" {
 description = "The Gihub OAuth app secret"
}
