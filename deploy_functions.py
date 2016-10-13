def deployApplicaton(oldName, newName, servers, package, plan)
  print 'Stopping and undeploying ' + oldName
  stopApplication(oldName)
  undeploy(oldName)

  appServers = servers.join(',')
  print 'Deploying ' + newName + ' to: ' + appServers
  progress = deploy(appName=newName, path=package, targets=appServers, planPath=plan)
  progress.printStatus()
  print 'Starting ' + newName
  progress = startApplication(newName)
  progress.printStatus()



