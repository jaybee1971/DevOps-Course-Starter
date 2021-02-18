### use case diagram
@startuml
left to right direction
actor "User" as fc
rectangle "ToDo App" {
  usecase "Review ToDos" as UC1
  usecase "Add ToDo" as UC2
  usecase "Manage ToDos" as UC3
}
fc --> UC1
fc --> UC2
fc --> UC3
@enduml
