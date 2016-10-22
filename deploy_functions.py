
def undeployApplication(name):
  print 'Stopping and undeploying ' + name
  progress = stopApplication(name)
  progress.printStatus()
  progress = undeploy(name)
  progress.printStatus()


def deployApplication(oldName, newName, targets, package, plan=None):
  if oldName:
    undeployApplication(oldName)

  if isinstance(targets, list):
    print '- Deploying: ' + newName + ' to: [' + ', '.join(targets) + ']'
  else
    print '- Deploying: ' + newName + ' to: ' + targets

  progress = deploy(appName=newName, path=package, targets=targets, planPath=plan)
  progress.printStatus()
  #print 'Starting ' + newName
  #progress = startApplication(newName)
  #progress.printStatus()



