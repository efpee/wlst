
def undeployApplication(name)
  print 'Stopping and undeploying ' + name
  progress = stopApplication(name)i
  progress.printStatus()
  progress = undeploy(name)
  progress.printStatus()


def deployApplication(oldName, newName, servers, package, plan=None)
  if oldName:
    undeployApplication(oldName)

  appServers = servers.join(',')
  print 'Deploying ' + newName + ' to: ' + appServers
  progress = deploy(appName=newName, path=package, targets=appServers, planPath=plan)
  progress.printStatus()
  #print 'Starting ' + newName
  #progress = startApplication(newName)
  #progress.printStatus()



