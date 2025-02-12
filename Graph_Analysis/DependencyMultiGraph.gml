graph [
  directed 1
  multigraph 1
  node [
    id 0
    label "webapp"
  ]
  node [
    id 1
    label "workshopmanagementapi"
  ]
  node [
    id 2
    label "customermanagementapi"
  ]
  node [
    id 3
    label "invoiceservice"
  ]
  node [
    id 4
    label "mailserver"
  ]
  node [
    id 5
    label "rabbitmq"
  ]
  node [
    id 6
    label "sqlserver"
  ]
  node [
    id 7
    label "timeservice"
  ]
  node [
    id 8
    label "vehiclemanagementapi"
  ]
  node [
    id 9
    label "workshopmanagementeventhandler"
  ]
  node [
    id 10
    label "auditlogservice"
  ]
  node [
    id 11
    label "notificationservice"
  ]
  edge [
    source 0
    target 1
    key "call"
    edge "call"
  ]
  edge [
    source 0
    target 8
    key "call"
    edge "call"
  ]
  edge [
    source 0
    target 2
    key "call"
    edge "call"
  ]
  edge [
    source 1
    target 6
    key "call"
    edge "call"
  ]
  edge [
    source 1
    target 6
    key "WorkshopPlanningCreated"
    edge "WorkshopPlanningCreated"
  ]
  edge [
    source 1
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 1
    target 5
    key "WorkshopPlanningCreated"
    edge "WorkshopPlanningCreated"
  ]
  edge [
    source 2
    target 6
    key "call"
    edge "call"
  ]
  edge [
    source 2
    target 6
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 2
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 2
    target 5
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 3
    target 6
    key "call"
    edge "call"
  ]
  edge [
    source 3
    target 6
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 3
    target 6
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 3
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 3
    target 4
    key "call"
    edge "call"
  ]
  edge [
    source 5
    target 10
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 5
    target 10
    key "VehicleRegistered"
    edge "VehicleRegistered"
  ]
  edge [
    source 5
    target 10
    key "WorkshopPlanningCreated"
    edge "WorkshopPlanningCreated"
  ]
  edge [
    source 5
    target 10
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 5
    target 10
    key "DayHasPassed"
    edge "DayHasPassed"
  ]
  edge [
    source 5
    target 10
    key "MaintenanceJobFinished"
    edge "MaintenanceJobFinished"
  ]
  edge [
    source 5
    target 3
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 5
    target 3
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 5
    target 3
    key "MaintenanceJobFinished"
    edge "MaintenanceJobFinished"
  ]
  edge [
    source 5
    target 3
    key "DayHasPassed"
    edge "DayHasPassed"
  ]
  edge [
    source 5
    target 11
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 5
    target 11
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 5
    target 11
    key "DayHasPassed"
    edge "DayHasPassed"
  ]
  edge [
    source 5
    target 11
    key "MaintenanceJobFinished"
    edge "MaintenanceJobFinished"
  ]
  edge [
    source 5
    target 9
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 5
    target 9
    key "VehicleRegistered"
    edge "VehicleRegistered"
  ]
  edge [
    source 5
    target 9
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 5
    target 9
    key "MaintenanceJobFinished"
    edge "MaintenanceJobFinished"
  ]
  edge [
    source 7
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 8
    target 6
    key "call"
    edge "call"
  ]
  edge [
    source 8
    target 6
    key "VehicleRegistered"
    edge "VehicleRegistered"
  ]
  edge [
    source 8
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 8
    target 5
    key "VehicleRegistered"
    edge "VehicleRegistered"
  ]
  edge [
    source 9
    target 6
    key "call"
    edge "call"
  ]
  edge [
    source 9
    target 6
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 9
    target 6
    key "VehicleRegistered"
    edge "VehicleRegistered"
  ]
  edge [
    source 9
    target 6
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 9
    target 6
    key "MaintenanceJobFinished"
    edge "MaintenanceJobFinished"
  ]
  edge [
    source 9
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 9
    target 5
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 9
    target 5
    key "MaintenanceJobFinished"
    edge "MaintenanceJobFinished"
  ]
  edge [
    source 10
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 11
    target 6
    key "call"
    edge "call"
  ]
  edge [
    source 11
    target 6
    key "CustomerRegistered"
    edge "CustomerRegistered"
  ]
  edge [
    source 11
    target 6
    key "MaintenanceJobPlanned"
    edge "MaintenanceJobPlanned"
  ]
  edge [
    source 11
    target 6
    key "DayHasPassed"
    edge "DayHasPassed"
  ]
  edge [
    source 11
    target 5
    key "call"
    edge "call"
  ]
  edge [
    source 11
    target 5
    key "DayHasPassed"
    edge "DayHasPassed"
  ]
  edge [
    source 11
    target 4
    key "call"
    edge "call"
  ]
]
